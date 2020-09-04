class Compare:
    def eqls(self,actual,expected):
        '''

        :param actual: 实际结果
        :param expected: 预期结果
        :return:
        '''
        return  actual==expected

    def lt(self, actual, expected):
        '''

        :param actual: 实际结果
        :param expected: 预期结果
        :return:
        '''
        return actual < expected

    def lte(self, actual, expected):
        '''

        :param actual: 实际结果
        :param expected: 预期结果
        :return:
        '''
        return actual <= expected

    def gt(self, actual, expected):
        '''

        :param actual: 实际结果
        :param expected: 预期结果
        :return:
        '''
        return actual > expected

    def gte(self, actual, expected):
        '''

        :param actual: 实际结果
        :param expected: 预期结果
        :return:
        '''
        return actual >= expected
