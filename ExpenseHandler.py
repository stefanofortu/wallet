import numpy as np


class ExpenseCategory:
    def __init__(self, name, parent=None):
        self.name = name
        self.has_child = False
        self.child_list = []
        self.parent = parent
        if parent is None:
            self.level = 1
        else:
            self.level = None


class ExpenseHandler:
    def __init__(self):
        self.all_category = []
        self.create_categories()
        self.create_hierarchy()

    def create_hierarchy(self):
        for parent in self.all_category:
            for child in self.all_category:
                if child.parent is not None:
                    if parent.name == child.parent:
                        parent.has_child = True
                        parent.child_list.append(child.name)

        for child in self.all_category:
            for parent in self.all_category:
                if len(parent.child_list) > 0:
                    if child.name in parent.child_list:
                        try:
                            child.level = parent.level + 1
                        except:
                            print(parent.name, parent.level, child.name)
                            exit()

    def print_all(self):
        for c in self.all_category:
            print(c.name, "has child", c.has_child, c.child_list, "level", str(c.level))

    def get_category_list_names(self):
        res = [expense for expense in self.all_category]
        return res

    def get_level_category_list(self, level):
        level_category_list = []
        for c in self.all_category:
            if c.level == level:
                level_category_list.append(c)
        return level_category_list

    def create_categories(self):
        self.all_category.extend([ExpenseCategory(name="Cibo & Bevande", parent=None),
                ExpenseCategory(name="Bar & Locali", parent="Cibo & Bevande"),
                ExpenseCategory(name="Lunch", parent="Cibo & Bevande"),
                ExpenseCategory(name="Spesa", parent="Cibo & Bevande"),

                ExpenseCategory(name="Shopping", parent=None),
                ExpenseCategory(name="Abbigliamento & Scarpe", parent="Shopping"),
                ExpenseCategory(name="Electronics", parent="Shopping"),
                ExpenseCategory(name="Gifts", parent="Shopping"),

                ExpenseCategory(name="Home", parent=None),
                ExpenseCategory(name="Affitto/Mutuo", parent="Home"),
                ExpenseCategory(name="Energia, Utenze", parent="Home"),
                ExpenseCategory(name="Family", parent="Home"),
                ExpenseCategory(name="Furniture, Maintenance", parent="Home"),

                ExpenseCategory(name="Trasporti", parent=None),
                ExpenseCategory(name="Trasporto pubblico", parent="Trasporti"),

                ExpenseCategory(name="Veicoli", parent=None),
                ExpenseCategory(name="Assicurazione veicoli", parent="Veicoli"),
                ExpenseCategory(name="Carburante", parent="Veicoli"),
                ExpenseCategory(name="Manutenzione veicoli", parent="Veicoli"),
                ExpenseCategory(name="Parking and Tolls", parent="Veicoli"),

                ExpenseCategory(name="Entertainment", parent=None),
                ExpenseCategory(name="Eventi", parent="Entertainment"),
                ExpenseCategory(name="Fun", parent="Entertainment"),
                ExpenseCategory(name="Hobby", parent="Entertainment"),
                ExpenseCategory(name="Personal Care", parent="Entertainment"),
                ExpenseCategory(name="Sport, fitness", parent="Entertainment"),
                ExpenseCategory(name="Travel & Holidays", parent="Entertainment"),
                ExpenseCategory(name="Summer Holidays", parent="Travel & Holidays"),
                ExpenseCategory(name="Weekends", parent="Travel & Holidays"),

                ExpenseCategory(name="Spese finanziarie", parent=None),
                ExpenseCategory(name="Beneficienza", parent="Spese finanziarie"),
                ExpenseCategory(name="Salute", parent="Spese finanziarie"),

                ExpenseCategory(name="Investimenti", parent=None),
                ExpenseCategory(name="Education", parent="Investimenti"),
                ExpenseCategory(name="Work", parent="Investimenti"),
                ExpenseCategory(name="Beni immobili", parent="Investimenti"),
                ExpenseCategory(name="Education_New", parent="Investimenti"),
                ExpenseCategory(name="Work_New", parent="Investimenti"),

                ExpenseCategory(name="Introiti", parent=None),
                ExpenseCategory(name="Entrate da affitto", parent="Introiti"),
                ExpenseCategory(name="Interessi, Dividendi", parent="Introiti"),
                ExpenseCategory(name="Refunds", parent="Introiti"),
                ExpenseCategory(name="Salary", parent="Introiti"),

                ExpenseCategory(name="Altro", parent=None),
                ExpenseCategory(name="Correzioni", parent="Altro"),
                ExpenseCategory(name="Prelievo", parent="Altro"),
                ExpenseCategory(name="Trasferimento", parent="Altro"),
                ExpenseCategory(name="Correzioni", parent="Altro"),
                ExpenseCategory(name="Prelievo", parent="Altro"),
                ExpenseCategory(name="Trasferimento", parent="Altro"),
                ExpenseCategory(name="Salary IN", parent="Altro"),
                ExpenseCategory(name="Salary OUT", parent="Altro"),
                ExpenseCategory(name="Unexpected", parent="Altro"),
                ExpenseCategory(name="Placeholder", parent="Altro")
            ])
