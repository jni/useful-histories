# IPython log file
# Run this in the NewEM data folder


from gala import classify
X, y = classify.load_training_data_from_disk('training-data-0.h5',
        names=['data', 'labels'])
        
train_idxs = np.random.randint(0, X.shape[0], size=10_000)
y = y[:, 0]
Xtr, ytr = X[train_idxs], y[train_idxs]
test_idxs = np.random.randint(0, X.shape[0], size=1000)
test_idxs = np.setdiff1d(test_idxs, train_idxs)
Xts, yts = X[test_idxs], y[test_idxs]
rf = classify.default_random_forest()
# get_ipython().magic('timeit -n 1 -r 1 rf.fit(Xtr, ytr)')
lg = classify.get_classifier('logist')
# get_ipython().magic('timeit -n 1 -r 1 lg.fit(Xtr, ytr)')
# 20x faster training
lgacc = 1 - np.sum(lg.predict(Xts) != yts) / len(yts)
# 73%
rfacc = 1 - np.sum(rf.predict(Xts) != yts) / len(yts)
# 79.2%
# get_ipython().magic('timeit -r 1 -n 1 lg.predict(Xts)')
# get_ipython().magic('timeit -r 1 -n 1 rf.predict(Xts)')
# 20x faster prediction
# get_ipython().magic('timeit rf.predict(Xts[0:1])')
# get_ipython().magic('timeit lg.predict(Xts[0:1])')
# 30x faster single line prediction
from sklearn.preprocessing import StandardScaler
s = StandardScaler()
Xtrn = s.fit_transform(Xtr)
from sklearn import pipeline
lg = classify.get_classifier('logist')
lg.fit(Xtrn, ytr)
lg2 = pipeline.make_pipeline(s, lg)
lgacc2 = 1 - np.sum(lg2.predict(Xts) != yts) / len(yts)
# 79.6% (!!!)
lg3 = pipeline.make_pipeline(StandardScaler(),
                             classify.get_classifier('logist'))
                             
lg3 = lg3.fit(Xtr, ytr)
lgacc3 = 1 - np.sum(lg3.predict(Xts) != yts) / len(yts)
# 79.6%
