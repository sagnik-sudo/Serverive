from minio import Minio
from minio.error import S3Error

from src.config import Configurations


class MinioTransactions:
    def __init__(self):
        """
        Initializes the MinioClient"""
        self.config = Configurations()
        self.minioClient = Minio(self.config.endpoint,
                                 access_key=self.config.accessKey,
                                 secret_key=self.config.secretKey,
                                 secure=False)

    def createBucket(self, bucketName):
        """
        Creates a bucket"""
        try:
            self.minioClient.make_bucket(bucketName)
        except S3Error as err:
            print(err)
            Exception(err)
        return True

    def deleteBucket(self, bucketName):
        """
        Deletes a bucket"""
        try:
            self.minioClient.remove_bucket(bucketName)
        except S3Error as err:
            print(err)
            Exception(err)
        return True

    def uploadFile(self, bucketName, filePath, fileName):
        """
        Uploads a file to a bucket"""
        try:
            self.minioClient.fput_object(bucketName, fileName, filePath)
        except S3Error as err:
            print(err)
            Exception(err)
        return True

    def downloadFile(self, bucketName, fileName):
        """
        Downloads a file from a bucket"""
        try:
            obj = self.minioClient.get_object(bucketName, fileName)
            return obj.data
        except S3Error as err:
            print(err)
            Exception(err)

    def deleteFile(self, bucketName, fileName):
        """
        Deletes a file from a bucket"""
        try:
            self.minioClient.remove_object(bucketName, fileName)
        except S3Error as err:
            print(err)
            Exception(err)
        return True

    def listBuckets(self):
        """
        Lists all buckets"""
        try:
            return self.minioClient.list_buckets()
        except S3Error as err:
            print(err)
            Exception(err)

    def listObjects(self, bucketName):
        """
        Lists all objects in a bucket"""
        try:
            return self.minioClient.list_objects(bucketName)
        except S3Error as err:
            print(err)
            Exception(err)

    def bucketExists(self, bucketName):
        """
        Checks if a bucket exists"""
        try:
            return self.minioClient.bucket_exists(bucketName)
        except S3Error as err:
            print(err)
            Exception(err)
