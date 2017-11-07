from standard_tranche import StandardTranche



def main():
    t = StandardTranche(100000, 0.05, 1)
    t.increase_time_period()
    t.increase_time_period()
    print t._transactions


if __name__ == "__main__":
    main()
