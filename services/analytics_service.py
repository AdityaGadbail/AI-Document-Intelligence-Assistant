
from repositories.analytics_repository import AnalyticsRepository

class AnalyticsService:

    @staticmethod
    def get_dashboard_statistics(db,user_id):

        stats = AnalyticsRepository.get_dashboard_statistics(db,user_id=user_id)

        storage_mb = round(stats["storage"] / (1024 * 1024),2) 

        stats["storage"] = storage_mb

        return stats

    @staticmethod
    def get_upload_activity(db,user_id):
        return AnalyticsRepository.get_upload_activity(db=db,user_id=user_id)

    @staticmethod
    def get_document_pages(db, user_id):
        return AnalyticsRepository.get_document_pages(db,user_id)

    @staticmethod
    def get_status_distribution(db, user_id):
        return AnalyticsRepository.get_status_distribution(db,user_id)