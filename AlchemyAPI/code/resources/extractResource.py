from flask_restful import Resource, reqparse
from extractor import Extractor 

extractor = Extractor()

class ExtractResource(Resource):

    parser = reqparse.RequestParser() #Condicoes de entrada
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('count',
    type=int,
    required=True,
    help="This field cannot be left blank!"
    )

    def post(self):

        data = self.parser.parse_args()

        username = data['username']
        count = data['count']

        extractor.generate_twitter_df(username,count)
        extractor.preprocessing()
        extractor.save_df()

        return {
            'username': username,
            'tweets_extracted': extractor.tweets_extracted,
            'filename': extractor.filename
            }




