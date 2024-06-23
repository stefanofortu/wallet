class CategoryStructure:
    categories = {"Cibo & Bevande": ["Bar & Locali", "Lunch", "Spesa"],
                  "Shopping": ["Abbigliamento & Scarpe", "Electronics", "Gifts"],
                  "Home": ["Affitto/Mutuo", "Energia & Utenze", "Family", "Furniture, Maintenance"],
                  "Trasporti": ["Trasporto pubblico"],
                  "Veicoli": ["Assicurazione veicoli", "Carburante", "Manutenzione veicoli", "Parking and Tolls"],
                  "Entertainment": ["Eventi", "Fun", "Hobby", "Personal Care",
                                    "Sport & Fitness", "Summer Holidays", "Weekends"],
                  "Travel & Holidays": ["Summer Holidays", "Weekends"],
                  "Spese finanziarie": ["Beneficienza", "Salute"],
                  "Investimenti": ["Education", "Work", "Beni immobili", "Education_New", "Work_New"],
                  "Introiti": ["Entrate da affitto", "Interessi, Dividendi", "Refunds", "Salary"],
                  "Altro": ["Correzioni", "Prelievo", "Trasferimento", "Correzioni", "Prelievo",
                            "Trasferimento", "Salary IN", "Salary OUT", "Unexpected", "Placeholder", "Adjust balance"]
                  }

    expense_groups = {"Essenziali_Dovute": {"Bollette_Manutenzione": ["Energia & Utenze", "Furniture, Maintenance",
                                                                    "Family", "Affitto/Mutuo", ],
                                          "Macchina": ["Assicurazione veicoli", "Manutenzione veicoli"],
                                          "Salute_Beneficienza": ["Salute", "Beneficienza"]
                                          },
                    "Indispensabili_Necessità": {"Spesa_Caffe_Lunch": ["Bar & Locali", "Lunch", "Spesa"],
                                                 "Trasporti": ["Trasporto pubblico", "Carburante", "Parking and Tolls"],
                                                 "Future": ["Work_New", "Education_New"]
                                                 },
                    "Volute_NonEssenziali": {"Selfcare(Clothes & Sport)": ["Abbigliamento", "Gifts",
                                                                           "Personal Care", "Sport & Fitness"],
                                             "Fun & Hobbies": ["Electronics", "Fun", "Hobby",
                                                              "Adjust balance", "Unexpected"],
                                             "Travel & Events": ["Eventi", "Summer Holidays", "Weekends"]
                                             }
                    }

    @staticmethod
    def get_category_structure():
        return CategoryStructure.categories

    @staticmethod
    def get_basic_categories():
        category_list = []
        for c in CategoryStructure.categories.keys():
            category_list.extend(CategoryStructure.categories[c])

        return category_list

    @staticmethod
    def get_expenses_groups():
        return CategoryStructure.expense_groups
