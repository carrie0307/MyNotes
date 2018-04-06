# -*- coding: utf-8 -*-

def find132pattern(nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        ak = float("-inf")
        st = []
        for i in reversed(xrange(len(nums))):
            if nums[i] < ak:
                print '---'
                return True
            else:
                while st and nums[i] > st[-1]:
                    print '==='
                    ak = st.pop()
            st.append(nums[i])
        return False


if __name__ == '__main__':
    print find132pattern([-1, 3, 2, 0])
