import copy
from itertools import product


class FindG:
    def __init__(self, all_attr):
        self.all_attributes = all_attr

        most_general_h = []
        for _ in range(len(all_attr)):
            most_general_h.append('?')
        self.the_most_general_h = tuple(most_general_h)

    @staticmethod
    def are_all_attributes_the_same(hypothesis, instance):
        """
        This method ignores all '?'s
        :param hypothesis:
        :param instance:
        :return:
        """
        if len(hypothesis) != len(instance):
            raise ValueError('different length')

        for i in range(len(hypothesis)):
            if hypothesis[i] != '?':
                if hypothesis[i] != instance[i]:
                    return False
        return True

    def is_hypothesis_the_most_general(self, hypothesis):
        if hypothesis == self.the_most_general_h:
            return True
        return False

    def replace_all_general_attribute_with_others(self, hypothesis, instance):

        num_general_attr = 0
        for a in hypothesis:
            if a == '?':
                num_general_attr += 1

        other_attributes = []
        for i in range(len(hypothesis)):
            if hypothesis[i] != '?':
                other_attributes.append([hypothesis[i]])
            else:
                new_attrs = []
                for attr in self.all_attributes[i]:
                    if attr != instance[i]:
                        new_attrs.append(attr)
                if num_general_attr > 1:
                    new_attrs.append('?')
                other_attributes.append(new_attrs)
        return other_attributes

    @staticmethod
    def make_cartesian_product(my_list):
        """
        making cartesian product of list elements which are list themselves
        :param my_list:
        :return:
        """
        p = my_list[0]
        for i in range(1, len(my_list)):
            pr = list(product(p, my_list[i]))
            pr_new = []
            if i == 1:
                p = copy.deepcopy(pr)
            else:
                for e in pr:
                    temp_list = list(e[0])
                    temp_list.append(e[1])
                    pr_new.append(temp_list)
                p = copy.deepcopy(pr_new)
        return p

    def remove_less_general_hypotheses(self, temporary_G):

        if len(temporary_G) == 1:
            return temporary_G
        elif self.the_most_general_h in temporary_G:
            general_hypothesis = set()
            general_hypothesis.add(self.the_most_general_h)
            return general_hypothesis

        new_General = set()
        for h in temporary_G:
            less_general_flag = False
            for hy in temporary_G:
                if h != hy and self.is_less_general(h, hy):
                    less_general_flag = True
                    break
            if not less_general_flag:
                new_General.add(h)

        return new_General

    @staticmethod
    def is_less_general(h1, h2):
        for i in range(len(h1)):
            if h1[i] == '?' and h2[i] != '?':
                return False
            if h1[i] != '?' and h2[i] != '?' and h1[i] != h2[i]:
                return False
        return True

    def find_g(self, Data):
        G = set()
        G.add(self.the_most_general_h)

        # Getting negative examples
        negative_examples = {}
        for key, value in Data.items():
            if value == 0:
                negative_examples[key] = value

        if len(negative_examples) == 0:
            return G

        for example in negative_examples:
            current_G = set()
            for h in G:
                if '?' not in h:
                    if h != example:
                        current_G.add(h)
                else:
                    if self.is_hypothesis_the_most_general(h) or self.are_all_attributes_the_same(h, example):
                        possible_attribute_list = fg.replace_all_general_attribute_with_others(h, example)

                        forbidden_hypo = []
                        for i in range(len(possible_attribute_list)):
                            if len(possible_attribute_list[i]) == 1:
                                forbidden_hypo.append(possible_attribute_list[i][0])
                            else:
                                forbidden_hypo.append('?')

                        possible_hypotheses = self.make_cartesian_product(possible_attribute_list)

                        if forbidden_hypo in possible_hypotheses:
                            possible_hypotheses.remove(forbidden_hypo)

                        for hypo in possible_hypotheses:
                            current_G.add(tuple(hypo))
                    else:
                        current_G.add(h)
            if self.the_most_general_h in current_G:
                current_G.remove(self.the_most_general_h)

            G = copy.deepcopy(self.remove_less_general_hypotheses(current_G))

        return G


if __name__ == "__main__":
    all_attributes_list = [['S', 'C', 'R'], ['W', 'C'], ['N', 'H'], ['S', 'W'], ['W', 'C'], ['S', 'C']]
    fg = FindG(all_attributes_list)

    Data_set = {('S', 'W', 'N', 'S', 'W', 'S'): 1, ('S', 'W', 'H', 'S', 'W', 'S'): 1,
                ('R', 'C', 'H', 'S', 'W', 'C'): 0, ('S', 'W', 'H', 'S', 'C', 'C'): 1,
                ('S', 'W', 'N', 'W', 'W', 'S'): 0}

    G_boundary = fg.find_g(Data_set)
    print(" \n final G_boundary: ", G_boundary)
    print(" len(G_boundary): ", len(G_boundary))





