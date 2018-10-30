import pymongo

# Decimal places checks
def validator_decimal(num, min, max, decimal_places):
	if float(num) >= float(min) and float(num) <= float(max):
		return True, round(float(num), decimal_places)
	return False, float(num)

# Float checks
def is_float(num):
	try:
		result = float(num)
		return True
	except:
		return False

def save_structured_file(value):
	client = pymongo.MongoClient(host='localhost', port=27017)
	db = client['myTest2']
	collection = db['file_structured']
	# file = {
	# 	'id': '20170101',
	#     'name': 'Jordan',
	#     'age': 20,
	#     'gender': 'male'
	# }
	retult = collection.insert(value)

def byte_to_string(b):
    try:
        return b.decode("utf-8")
    except ValueError:
        return b