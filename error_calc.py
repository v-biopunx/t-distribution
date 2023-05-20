from decimal import *
import sys


class DirectMeasures:
    def __init__(self, numbers, syst_err):
        self.numbers = numbers
        self.syst_err = Decimal(syst_err)

    def confidence_interval(self):
        self.numbers = [Decimal(number) for number in self.numbers]
        mean = sum(self.numbers) / len(self.numbers)
        separate_errs = [(dec - mean) for dec in self.numbers]
        sqr_errs = [x**2 for x in separate_errs]
        quad_mean = (sum(sqr_errs) /
                     (len(self.numbers) *
                      (len(self.numbers) - 1)))**Decimal('0.5')
        for err in separate_errs:
            # Exclude blunders from initial measurement list
            # and recalculate quadratic mean without them
            if abs(err) > 4*quad_mean:
                del self.numbers[separate_errs.index(err)]
                return self.confidence_interval()
        student = {2: "12.71", 3: "4.30", 4: "3.18", 5: "2.78", 6: "2.57",
                   7: "2.45", 8: "2.36", 9: "2.31", 10: "2.26", 11: "2.00"}
        random_err = Decimal(student[len(self.numbers)]) * quad_mean
        # Find a corresponding Student coefficient
        # for the number of measurements and calculate relative error
        if random_err > self.syst_err*1000:
            error = random_err
        elif self.syst_err > random_err*1000:
            error = self.syst_err
        else:
            error = Decimal.sqrt((self.syst_err**Decimal('2') +
                                  random_err**Decimal("2")))
        relative_err = (error / mean)*Decimal("100")

        # Write verbose calculations to a text file
        s = (f'Confidence interval is {mean.quantize(Decimal("1.000"))} ' +
             f'+- {error.quantize(Decimal("1.000"))} units. ' +
             f'Relative error is {relative_err.quantize(Decimal("1.00"))} %')
        sys.stdout = open("error_calculations.txt", "w")
        print(f'{len(self.numbers)} measurements are accurate.')
        print('')
        print('Accurate measurements:')
        for num in self.numbers:
            print(f'{num.quantize(Decimal("1.000"))} units, ', end='')
        print(
            f'arithmetic mean = {mean.quantize(Decimal("1.000"))} units\n')
        print('Separate errors for each measurement:')
        for err in separate_errs:
            print(f'{err.quantize(Decimal("1.000000"))} units, ', end='')
        print('\n')
        print('Squares of each error:')
        for err in sqr_errs:
            print(
                f'{err.quantize(Decimal("1.000000"))} sqr.units, ', end='')
        print('\n')
        print(f'Quadratic mean: {quad_mean.quantize(Decimal("1.000000"))}'
              + f' units.\n')
        print(f'Random error: {student[len(self.numbers)]} * ' +
              f'{quad_mean.quantize(Decimal("1.000000"))} = ' +
              f'{random_err.quantize(Decimal("1.000000"))} units\n')
        print(s)


print('Welcome to direct measurement error calculator')
print('Please enter your measurements, using a point ' +
      '\nto separate integer and fraction parts of a decimal' +
      '\nand separating individual numbers with a comma and a space:')
numbers = input()
number_list = numbers.split(', ')
print('Please enter the systematic error of your measurement device:')
systematic_error = input()
measurement = DirectMeasures(number_list, systematic_error)
print(f'Step by step error calculations are located' +
      f' at {sys.path[0]}\error_calculations.txt\n' +
      f'Press enter to exit')
exit_key = input()  # Close the window after the script has been executed
try:
    print(measurement.confidence_interval())
except ValueError:
    pass
