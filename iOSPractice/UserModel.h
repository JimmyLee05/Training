#import <Foundation/Foundation.h>

@interface UserModel : NSObject
@property(nonatomic,copy)NSString* uid;
@property(nonatomic,copy)NSString* username;
@property(nonatomic,copy)NSString* userpk;
@property(nonatomic,copy)NSString* realname;
@property(nonatomic,copy)NSString* acatar;
@property(nonatomic,copy)NSString* height;
@property(nonatomic,copy)NSString* weight;
@property(nonatomic,copy)NSString* sex;
@property(nonatomic,copy)NSString* birth;

-(instancetype)initWithDirectionary:(NSDictionary*)dict;

@end
