class Solution:
    def maxProfit(self, prices):
        if len(prices) == 1:
            return 0
        l = 0
        r = len(prices) - 1
        mx = 0
        while (l < r):
            if (prices[l] < prices[r]):
                mx = max(mx, prices[r] - prices[l])
                r -= 1

            elif (prices[r] < prices[l]):
                l += 1

            else:
                mx = max(mx, prices[r] - prices[l])
                l += 1
                r -= 1
        return mx


print(Solution().maxProfit([7, 1, 5, 3, 6, 4]))
