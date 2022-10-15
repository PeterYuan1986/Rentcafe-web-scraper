class Solution(object):
    def validPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        n=len(s)
        for i in range(n):
            if s[i]!=s[n-i-1]:
                x = s[:i]+s[i+1:]
                y= s[:n-i-1]+s[n-i-1+1:]

                return x == x[::-1] or y == y[::-1]
        return True

print(Solution().validPalindrome('abc'))