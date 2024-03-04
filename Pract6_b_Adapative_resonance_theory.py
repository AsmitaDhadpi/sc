from future import
division
importnumpyas np
fromneupy.utilsimportformat_data
fromneupy.core.propertiesimport (ProperFractionProperty,
IntProperty)
fromneupy.algorithms.baseimportBaseNetwork
 all = ('ART1',)
classART1(BaseNetwork):
"""
Adaptive Resonance Theory (ART1) Network for binary
data clustering.
Notes
- Weights are not random, so the result will be
always reproduceble.
Parameters
rho : float
Control reset action in training process. Value must be
between ``0`` and ``1``, defaults to ``0.5``.
n_clusters : int
Number of clusters, defaults to ``2``. Min value is also
``2``.
{BaseNetwork.Parameters}
Methods
train(X)
ART trains until all clusters are found.
predict(X)
Each prediction trains a new network. It's an alias to
the ``train`` method.
{BaseSkeleton.fit}
Examples
>>>import numpy as np
>>>from neupy import algorithms
>>>
>>>data = np.array([
... [0, 1, 0],
... [1, 0, 0],
... [1, 1, 0],
... ])
>>>>
>>>artnet = algorithms.ART1(
... step=2,
... rho=0.7,
... n_clusters=2,
... verbose=False
... )
>>>artnet.predict(data)
array([ 0., 1., 1.])
"""
rho =ProperFractionProperty(default=0.5)
n_clusters=IntProperty(default=2, minval=2)
deftrain(self, X):
X =format_data(X)
ifX.ndim!=2:
raiseValueError("Input value must be 2 dimensional, got "
"{}".format(X.ndim))
nsamples, n_features=X.shape
n_clusters=self.n_clusters
step =self.step
rho =self.rho
ifnp.any((X !=0) & (X !=1)):
raiseValueError("ART1 Network works only with binary
matrices")
ifnothasattr(self, 'weight_21'):
self.weight_21 =np.ones((n_features, n_clusters))
ifnothasattr(self, 'weight_12'):
scaler = step / (step +n_clusters-1)
self.weight_12 = scaler *self.weight_21.T
weight_21 =self.weight_21
weight_12 =self.weight_12
ifn_features!= weight_21.shape[0]:
raiseValueError("Input data has invalid number of features. "
"Got {} instead of {}"
"".format(n_features, weight_21.shape[0]))
classes =np.zeros(n_samples)
# Train network
fori, p inenumerate(X):
disabled_neurons= []
reseted_values= []
reset =True
while reset:
output1 = p
input2 = np.dot(weight_12, output1.T)
output2 =np.zeros(input2.size)
input2[disabled_neurons] =-np.inf
winner_index= input2.argmax()
output2[winner_index] =1
expectation = np.dot(weight_21, output2)
output1 =np.logical_and(p, expectation).astype(int)
reset_value= np.dot(output1.T, output1) / np.dot(p.T, p)
reset =reset_value< rho
if reset:
disabled_neurons.append(winner_index)
reseted_values.append((reset_value, winner_index))
iflen(disabled_neurons) >=n_clusters:
# Got this case only if we test all possible clusters
reset =False
winner_index=None
ifnot reset:
ifwinner_indexisnotNone:
weight_12[winner_index, :] = (step * output1) / (
step + np.dot(output1.T, output1) -1
)
weight_21[:, winner_index] = output1
else:
# Get result with the best `rho`
winner_index=max(reseted_values)[1]
classes[i] =winner_index
return classes
defpredict(self, X):
returnself.train(X)
