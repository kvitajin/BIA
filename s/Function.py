from numpy import exp
from numpy import sqrt
from numpy import sin
from numpy import cos
from numpy import e
from numpy import pi

VALID_FUNCTION_NAMES = [
	'ackley',
	'griewank',
	'sphere',
	'levy',
	'michalewicz',
	'rastrigin',
	'rosenbrock',
	'schwefel',
	'sphere',
	'zakharov'
]

class Function:
	def __init__(self, name):
		global VALID_FUNCTION_NAMES
		if name not in VALID_FUNCTION_NAMES:
			raise Exception('invalid function name:', name)
		self.name = name

	def ackley(self, params = []) -> float:
		a = 20
		b = 0.2
		c = 2 * pi
		d = 2
		sum_pow = 0
		sum_cos = 0
		for item in params:
			sum_pow += item**2
			sum_cos += cos(c * item)
		return -a * exp(-b * sqrt(1 / d * sum_pow)) - exp(1 / d * (sum_cos)) + a + e

	def griewank(self, params = []):
		sum1, sum2 = 0.0, 0.0
		for index, item in enumerate(params):
			sum1 += (item**2) / 4000
			sum2 *= cos(item / (sqrt(index + 1)))
		return sum1 - sum2 + 1

	def levy(self, params = []):
		dimension = len(params)
		w = 0.0
		w_d = 1 + (params[dimension - 1] - 1) / 4
		tmp = 0.0
		sum = 0.0
		for item in params:
			w = 1 + (item - 1) / 4
			tmp = ((w - 1)**2) * (1 + 10 * sin(pi * w + 1)**2) + (w_d - 1)**2 * (1 + sin(2 * pi * w_d))
			sum += tmp
		return sum

	def michalewicz(self, params = []):
		m = 10
		dimension = len(params)
		sum = 0.0
		for i in range(dimension):
			sum -= (sin(params[i]) * (sin((i * params[i]**2) / pi)**(2 * m)))
		return sum

	def rastrigin(self, params = []):
		dimension = len(params)
		return 10 * dimension + ((params[0]**2 - 10 * cos(2*pi*params[0])) + (params[1]**2 - 10 * cos(2*pi*params[1])))

	def rosenbrock(self, params = []):
		return 100*(params[1]-params[0]**2)**2+(params[0]-1)**2

	def schwefel(self, params = []):
		dimension = len(params)
		sum = 0.0
		for i in params:
			sum += i * sin(sqrt(abs(i)))
		return 418.9829 * dimension - sum

	def sphere(self, params = []) -> float:
		sum = 0
		for item in params:
			sum += item**2
		return (1 / 899) * (sum)

	def zakharov(self, params = []) -> float:
		dimension = len(params)
		sum1, sum2, sum3, result = 0.0, 0.0, 0.0, 0.0
		for i in range(dimension):
			sum1 = params[i] ** 2
			sum2 = (0.5 * i * params[i]) ** 2
			sum3 = (0.5 * i * params[i]) ** 4
			result += sum1 + sum2 + sum3
		return result

	def __call__(self, params = []) -> float:
		return getattr(self, self.name)(params)
