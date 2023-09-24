# import the necessary packages
from scipy.spatial import distance as dist
import numpy as np

class PillSearcher:
	def __init__(self, db):
		# store the pill database
		self.db = db

	def search(self, size, shape, color, texture, weights, eps=1e-10):
		# initialize the results dictionary
		results = {"size": {}, "shape": {}, "color": {},
			"texture": {}, "combined": {}}

		# loop over the database
		for pillID in self.db.keys():
			# compute the distance between the pill sizes
			sizeDist = dist.euclidean(size, self.db[pillID]["size"])
			results["size"][pillID] = sizeDist

			# compute the distance between the shape features
			shapeDist = dist.euclidean(shape,
				self.db[pillID]["shape"])
			results["shape"][pillID] = shapeDist

			# compute the distance between the color features
			colorDist = self.chi2_distance(color,
				self.db[pillID]["color"])
			results["color"][pillID] = colorDist

			# compute the distance bewteen the texture features
			textureDist = self.chi2_distance(texture,
				self.db[pillID]["texture"])
			results["texture"][pillID] = textureDist

		# loop over each set of search results
		for t in results.keys():
			# ignore the combined set of search results since they
			# are not yet populated
			if t == "combined":
				continue

			# find the largest similariy/distance score
			maxDist = max(results[t].values())

			# loop over all results again, this time scaling the
			# compute distance to the range [0, 1]
			for (pillID, d) in results[t].items():
				results[t][pillID] = d / (maxDist + eps)

		# loop over the database keys a second time, this time to
		# combine the search results
		for pillID in self.db.keys():
			# compute the weighted sum of distances
			d = np.sum([
				weights["size"] * results["size"][pillID],
				weights["shape"] * results["shape"][pillID],
				weights["color"] * results["color"][pillID],
				weights["texture"] * results["texture"][pillID],
			])
			results["combined"][pillID] = d

		# sort our results, so that the smaller distances (i.e. the
		# more similar pills) are at the front of the list
		results["combined"] = sorted([(v, k) for (k, v) in \
			results["combined"].items()])

		# return the set of combined pill results
		return results["combined"]

	def chi2_distance(self, histA, histB, eps=1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum(((histA - histB) ** 2) / (histA + histB + eps))

		# return the chi-squared distance
		return d