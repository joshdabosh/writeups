# Comprehensive-2
Rev, 65

>  Written by boomo
>  His power level increased... What do I do now?? comprehensive_2.py Output: [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65] 

This was also incredibly cursed but the cleaned up code ended up looking something like:
```py
print(str(
    [x for z in 
        [
            [
                [
                    ord(m[i]) ^ ord(n[j // 3]) ^ ord(n[i - j - k]) ^ ord(n[k // 21]) for i in range(j + k, j + k + 3)
                ] for j in range (0, 21, 3)
            ] for k in range(0, len(m), 21)
        ] for y in z for x in y
    ]
)[1:-1])
```
where `m` is a 63 character message and `n` is the 7 character key. Essentially, for each `i` in the range 0-63 (inclusive), the end result is `m[i] ^ n[i / 21] ^ n[(i % 21) / 3] ^ n[i % 3]`. Now, I tried to be smart about this then realized that `n` is brute-forceable, so I rewrote the whole thing in Rust so I could brute force it a bit faster:
```rust
const DATA_LEN: usize = 63;
static DATA: [u8; DATA_LEN] = [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65];
const N_LEN: usize = 7;
const NOTIFS: u64 = 100000000;

fn gen_indices(i: usize) -> (usize, usize, usize) {
    (i / 21, (i % 21) / 3, i % 3)
}

fn is_valid(c: u8) -> bool {
    return c >= b' ' && c <= b'/'
        || c >= b':' && c <= b'@'
        || c >= b'[' && c <= b'`'
        || c >= b'{' && c <= b'~'
        || c >= b'a' && c <= b'z';
}

fn decode(n: &[u8; N_LEN], indices: &[(usize, usize, usize); DATA_LEN]) -> Option<String> {
    let mut ret = String::new();
    let mut space_count = 0;
    let mut braced: u8 = 0;
    for i in 0..DATA_LEN {
        let (a, b, c) = indices[i];
        let chr = DATA[i] ^ n[a] ^ n[b] ^ n[c];
        if !is_valid(chr) {
            return None;
        }
        if chr == b' ' {
            space_count += 1;
            if space_count > 5 {
                return None;
            }
        }
        if chr == b'{' {
            if braced == 0 {
                braced = 1;
            } else {
                return None;
            }
        }
        if chr == b'}' {
            if braced == 1 {
                braced = 2;
            } else {
                return None;
            }
        }
        ret.push(chr as char);
    }
    if braced != 2 || space_count != 5 || !ret.contains("tjctf{") {
        return None;
    }
    Some(ret)
}

fn inc(n: &mut [u8; N_LEN]) -> bool {
    n[0] += 1;
    for i in 0..N_LEN {
        if n[i] > b'z' {
            if i == N_LEN - 1 {
                return false;
            } else {
                n[i + 1] += 1;
            }
            n[i] = b'a';
        } else {
            return true;
        }
    }
    return false;
}

fn main() {
    let mut indices: [(usize, usize, usize); DATA_LEN] = [(0, 0, 0); DATA_LEN];
    let mut cur_n: [u8; N_LEN] = [b'a'; N_LEN];
    let mut ind: u64 = 0;
    for i in 0..DATA_LEN {
        indices[i] = gen_indices(i);
    }
    while inc(&mut cur_n) {
        ind += 1;
        if ind % NOTIFS == 0 {
            println!("at index {}", ind / NOTIFS);
        }
        if let Some(s) = decode(&cur_n, &indices) {
            println!("found match {}", s);
        }
    }
}
```

Flag: `tjctf{sumimasen_flag_kudasaii}`

Make sure to compile with optimizations.

Remember,
> Rust is blazingly fast

;)