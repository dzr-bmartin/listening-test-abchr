from handlers.test_and_survey.audio_acr_test import AcrTestHandler, AcrSurveyHandler


class AbchrTestHandler(AcrTestHandler):
    async def prepare(self):
        self.user_id = await self.auth_current_user()
        self.taskCollectionName = 'abchrTests'
        self.surveyCollectionName = 'abchrSurveys'


class AbchrSurveyHandler(AcrSurveyHandler):
    def prepare(self):
        self.taskCollectionName = 'abchrTests'
        self.surveyCollectionName = 'abchrSurveys'
