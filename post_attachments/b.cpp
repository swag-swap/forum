/**
 *    author:  Swapnil Deshmukh
 *    created: 2024-01-30 20:39:24
**/
#include <bits/stdc++.h>
using namespace std; 
#define ll long long

#ifdef ONLINE_JUDGE
#define debug(...) 42
#else
#include "../../algo/debug.h"
#endif

void solve(){
    int n;cin>>n;
    vector<int> a(n),b(n);
   	vector<pair<int,int>> c(n);
    for(int i=0;i<n;i++)cin>>a[i];
    for(int i=0;i<n;i++)cin>>b[i];
    for(int i=0;i<n;i++){
    	c[i] = {a[i]+b[i], i};
    }
    sort(c.begin(),c.end());
    for(int i=0;i<n;i++)cout<<a[c[i].second]<<" ";
    cout<<endl;
	for(int i=0;i<n;i++)cout<<b[c[i].second]<<" ";
	cout<<endl;

}

int main()
{  
    #ifndef ONLINE_JUDGE 
    freopen("../../algo/input.txt","r",stdin);
    freopen("../../algo/output.txt","w",stdout);
    #endif 
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int tc;
    cin >> tc;
    while (tc--)
    {
        solve();
    } 

    return 0;
}