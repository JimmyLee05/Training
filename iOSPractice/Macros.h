#ifndef Macros_h
#define Macros_h

#define WIDTH [UIScreen mainScreen].bounds.size.width
#define HEIGHT [UIScreen mainScreen].bounds.size.height
#define UIColorFromRGB(rgbValue) [UIColor colorWithRed:((float)(((rgbValue) & 0xFF0000 >> 16))/255.0 green:((float)(((rgbValue) & 0xFF00) >> 8))/255.0 blue:((float)(((rgbValue) & 0xFF))/255.0 alpha:1.0]

#define WeakObj(o) __weak typeof(o) o##Weak = o;
#define StrongObj(o) __strong typeof(o) o##Strong = o;

#define UID @"UID"

#define TOKEN @"TOKEN"

#define FIRSTLAUNCHDATE @"LAUNCHDATE"

#define LASTSYNDATE @"LASTSYNDATE"

#define ISLOGIN @"ISLOGIN" 

#define USER @"USER"

#define UmengAppkey @"5740280ee0f55a5edc002836"
#define WEIXINAppID @"wxef505bdf677830a9"
#define WEIXINAppSecret @"28b49b8dcd84561d1307dfb6c0f3d8ed"

typedef void (^ReturnValueBlock) (id ReturnValue);

typedef void (^ErrorCodeBock) (id errorCode);

typedef void (^FailureBlock)(void);

#endif /* Macros_h */