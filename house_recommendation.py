# this script is for the calculation logic for house similarity
# recommendation only depends on user's history of liked rooms and disliked rooms
# room should be referred as its index which is also its order in the similarity matrix
import random

def calculate_sum_list(nested_list):
	if len(nested_list) > 0:
		return [sum(i) for i in zip(*nested_list)]
	return [0] * 125

def recommendation(room_like_list, room_dislike_list, viewed_list, available_list, weight_list = [1,1,1,1]):
	# room_like_list is a nested list, it takes a shape as 4 x k x m, where 4 represents
	# 4 room types, k is a constrain on numbers of rooms to consider, m is the number of 
	# total rooms, in the prototypt, m = 125
	# weight is a 1 x 4 vector, it is the weight for each room type
	# after the calculation, the result should be a single index of the room of recommendation

	liked_bedroom = room_like_list[0]
	liked_living_room = room_like_list[1]
	liked_kitchen = room_like_list[2]
	liked_bathroom = room_like_list[3]

	dis_bedroom = room_dislike_list[0]
	dis_living_room = room_dislike_list[1]
	dis_kitchen = room_dislike_list[2]
	dis_bathroom = room_dislike_list[3]

	score_liked_bedroom = calculate_sum_list(liked_bedroom) * weight_list[0]
	score_liked_living_room = calculate_sum_list(liked_living_room) * weight_list[1]
	score_liked_kitchen = calculate_sum_list(liked_kitchen) * weight_list[2]
	score_liked_bathroom = calculate_sum_list(liked_bathroom) * weight_list[3]

	score_liked = [sum(i) for i in zip(score_liked_bedroom, score_liked_living_room, score_liked_kitchen, score_liked_bathroom)]

	score_dis_bedroom = calculate_sum_list(dis_bedroom) * weight_list[0]
	score_dis_living_room = calculate_sum_list(dis_living_room) * weight_list[1]
	score_dis_kitchen = calculate_sum_list(dis_kitchen) * weight_list[2]
	score_dis_bathroom = calculate_sum_list(dis_bathroom) * weight_list[3]

	score_dis = [sum(i) for i in zip(score_dis_bedroom ,score_dis_living_room ,score_dis_kitchen ,score_dis_bathroom)]

	score = [x[0]-x[1] for x in zip(score_liked,score_dis)]

	index_score = zip(range(125), score)

	sort_index_score = sorted(index_score, key = lambda x:x[1], reverse = True)
    
	if sum(score) == 0: 
        # this is the case that didn't make any choice on preference
		pool = [x for x in available_list if x not in viewed_list]
		return random.choice(pool) # recommend randomly
    
	for index,value in sort_index_score:
		if index not in viewed_list and index in available_list:
			return index
	return None #no more house available