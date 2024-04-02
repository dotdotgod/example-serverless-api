from pydantic import BaseModel


class CodeDeliveryDetails(BaseModel):
    Destination: str
    DeliveryMedium: str
    AttributeName: str


class CognitoIdpResponse(BaseModel):
    CodeDeliveryDetails: CodeDeliveryDetails
