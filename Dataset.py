import redis

from Parser import Parser
from constants import UNASSIGNED_IMAGE, REDIS_HOST, REDIS_PASWORD


class Dataset(list):
    def __init__(self, dataset_letter):
        self.dataset_letter = dataset_letter
        super(Dataset, self).__init__()
        self.r = redis.Redis(host=REDIS_HOST,password=REDIS_PASWORD)

        for image in Parser.parse(dataset_letter):
            image.set_database_letter(self.dataset_letter)
            self.append(image)

    def append(self, image):
        super(Dataset, self).append(image)
        image_key = image.__hash__()  # lets make sure that it is in redis
        if (self.r.get(image_key) == None):
            print("image not in redis, adding (" + image_key + ")")
            self.r.set(image_key, UNASSIGNED_IMAGE)

    def get_safe(self, index):
        currently_assigned_to = self.r.get(self[index].__hash__())
        assert (currently_assigned_to == None)  # hopefully it hasn't somehow disappeared from redis
        if (currently_assigned_to == UNASSIGNED_IMAGE):
            return self[index]
        else:
            raise IOError("image is not currently free")
