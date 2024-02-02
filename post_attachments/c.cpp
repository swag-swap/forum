/**
 *    author:  Swapnil Deshmukh
 *    created: 2024-01-31 13:33:45
**/
#include <bits/stdc++.h>
using namespace std; 
#define ll long long

#ifdef ONLINE_JUDGE
#define debug(...) 42
#else
#include "../../algo/debug.h"
#endif

const int maxb = 60;

bool get_bit(int64_t a,int i)
{
    return a&(1ll<<i);
}

void solve(){
    int64_t a,b,r;
    cin >> a >> b >> r;
    int64_t x = 0;
    bool first_bit = 1;
    if(a > b)
        swap(a,b);
    for(int i = maxb-1;i >= 0;--i)
    {
        bool bit_a = get_bit(a,i);
        bool bit_b = get_bit(b,i);
        if(bit_a != bit_b)
        {
            if(first_bit)
            {
                first_bit = 0;
            }
            else
            {
                if(!bit_a && x+(1ll<<i) <= r)
                {
                    x += (1ll<<i);
                    a ^= (1ll<<i);
                    b ^= (1ll<<i);
                }
            }
        }
    }
    cout << b-a << "\n";

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