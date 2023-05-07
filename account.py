#Parse the Account tag
import logging
import utils

logger = logging.getLogger()

class Account:
    def __init__(self, lines=None):
        self.name = None
        self.type = None
        self.description = None
        self.transactions = []
        self.credit_limit = None
        self.statement_date = None
        self.statement_bal = None
        if lines:
            self.parse_qif(lines)

    def parse_qif(self, lines):
        for line in lines:
            field,value = utils.parse_field_and_value(line)
            if field is None:
                continue

            if field == 'N':
                self.name = value
            elif field == 'T':
                self.type = value
            elif field == 'D':
                self.description = value
            elif field == 'L':
                self.credit_limit = value
            elif field == '/':
                self.statement_date = value
            elif field == '$':
                self.statement_bal = value
            else:
                #ignore other commands
                logger.warning("Unknown parameter in account: {}".format(line))
                continue

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_type(self):
        if self.type == 'Port' or self.type == '401(k)/403(b)':
            return 'Invst'
        return self.type

    def __str__(self):
        return self.to_readable()

    def to_readable(self):
        return 'Name:{} Type:{} Tx:{}'.format(self.name, self.type, len(self.transactions))

    def to_qif(self, short=True):
        qifstr = 'N{}\n'.format(self.name)
        if not short:
            qifstr += 'T{}\n'.format(self.type)
        else:
            # print the standardized name
            qifstr += 'T{}\n'.format(self.get_type())
        if (not short) and self.credit_limit:
            qifstr += 'L{}\n'.format(self.credit_limit)
        qifstr += '^\n'
        return qifstr

    def to_dict(self):
        retdict = {}
        retdict['name'] = self.name
        retdict['type'] = self.get_type()
        if self.credit_limit:
            retdict['credit_limit'] = self.credit_limit
        return retdict

    def validate(self):
        pass
