from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    or_condition = []
    no_match = True
    for rule in rules:
        consequents = rule.consequent()
        if not isinstance(consequents, list):
            consequents = [consequents]
        for consequent in consequents:
            var_map = match(consequent, hypothesis)
            if var_map is None:
                continue

            no_match = False
            and_sub_condition = []
            if var_map == {}:
                and_sub_condition.append(AND())

            conditions = rule.antecedent()
            is_and = True
            if not isinstance(conditions, list):
                conditions = [conditions]
            if isinstance(conditions, OR):
                is_and = False

            for condition in conditions:
                pop_res = populate(condition, var_map)
                and_sub_condition.append(backchain_to_goal_tree(rules, pop_res))

            if is_and:
                or_condition.append(AND(and_sub_condition))
            else:
                or_condition.append(OR(and_sub_condition))

    if no_match:
        return hypothesis
    
    
    res = OR([hypothesis, OR(or_condition)])
    res = simplify(res)
    return res


# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
rules = [ IF( AND( '(?x) has (?y)','(?x) has (?z)' ),THEN( '(?x) has (?y) and (?z)' ) ),IF( '(?x) has rhythm and music',THEN( '(?x) could not ask for anything more' ) ) ]
hypo = 'gershwin could not ask for anything more'
print backchain_to_goal_tree(rules, hypo)
