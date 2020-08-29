#include <bits/stdc++.h>
using namespace std;
void print_vector(vector<vector<int> > v){
   cout << "[";
   for(int i = 0; i<v.size(); i++){
      cout << "[";
      for(int j = 0; j <v[i].size(); j++){
         cout << v[i][j] << ", ";
      }
      cout << "],";
   }
   cout << "]"<<endl;
}
class Solution {
  public:
   vector < vector <int> > res;
void solve(int idx, vector <int> &a, int b, vector <int> temp){
      if(b == 0){
         res.push_back(temp);
         return;
      }
      if(idx == a.size())return;
      if(b < 0)return;
      sort(a.begin(), a.end());
      for(int i = idx; i < a.size(); i++){
         if(i > idx && a[i] == a[i-1])continue;
         temp.push_back(a[i]);
         solve(i + 1, a, b - a[i], temp);
         temp.pop_back();
      }
   }
   vector<vector<int> > combinationSum2(vector<int> &a, int b) {
      res.clear();
      vector <int> temp;
      solve(0, a, b, temp);
      return res;
   }
};
int main(){
   Solution ob;
   vector<int> v = {199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499, 199, 299, 399, 499};
   print_vector(ob.combinationSum2(v, 7174)) ;
}
