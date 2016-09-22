import gensim, logging
from tm import TopicModelling

tm = TopicModelling()
# dataset = tm.prepare_data('Sample.csv', 2)

# model = gensim.models.Word2Vec(dataset, min_count=1)
# model.save('trained')

new_model = gensim.models.Word2Vec.load('trained')

print new_model.most_similar(negative=['water'])
print new_model['water']

print new_model.similarity('italy', 'planet')