#Monet Harkin - Flatten Array

def arrFlatten(arr, newarr):
	for x in xrange(0,len(arr)):
		if type(arr[x]) == int:
			newarr.append(arr[x])
		else:
			arrFlatten(arr[x], newarr) 
	return newarr

	
#above 'else' takes the index that is a list within the arr ex: [[2,3]] 
#to run through the function and append, then moves on to the next index

# Sample output to test

arr=[1,[2,3],4,5,6,[7,[8,9,[10,[11],12,13,14]]]]
newarr=[]

print arrFlatten(arr,newarr)
