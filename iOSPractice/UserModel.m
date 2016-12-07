#import "UserModel.h"

@implementation UserModel

-(instancetype)initWithDictionary:(NSDictionary *)dict{
	if (self = [super init]) {
		self.uid = dict[@"id"];
		self.username = dict[@"username"];
		self.realname = dict[@"realname"];
		self.height = dict[@"height"];
		self.weight = dict[@"weight"];
		self.sex = dict[@"sex"];
		self.birth = dict[@"birth"];
		self.avatar = dict[@"acatar"];
	}
	return self;
}

@end