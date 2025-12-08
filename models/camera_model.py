class Camera:
    def __init__(self, companyId, name, location, ipAddress,
                 userName, password="", subnetMask="", defaultGateway=""):
        self.companyId = companyId
        self.name = name
        self.location = location
        self.ipAddress = ipAddress
        self.userName = userName
        self.password = password
        self.subnetMask = subnetMask
        self.defaultGateway = defaultGateway
