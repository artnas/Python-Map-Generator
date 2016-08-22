class Color:

    # 0 -> 255

    r = 0.0;
    g = 0.0;
    b = 0.0;
    a = 1.0;

    def __init__(self, r = 0.0, g = 0.0, b = 0.0):
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = 1;
    def GetTuple(self):
        return (int(self.r),int(self.g),int(self.b));
    def SetColor(self, r, g, b):
        self.r = r;
        self.g = g;
        self.b = b;
    def Copy(self, color):
        self.r = color.r;
        self.g = color.g;
        self.b = color.b;
    def SetWhite(self):
        self.SetColor(1,1,1);
    def SetBlack(self):
        self.SetColor(0,0,0);
    def SetColorFromGrayscale(self, f = 0.0):
        self.SetColor(f,f,f);

paperColor = Color(212, 161, 104);
waterColor = Color(0, 20, 28);

