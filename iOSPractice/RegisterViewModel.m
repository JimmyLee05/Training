#import "RegisterViewModel.h"
#import "UserModel.h"

@interface RegisterViewModel()

@property (nonatomic, strong, readwrite)NSNumber *invalid;

@property (nonatomic, copy, readwrite)NSString *invalidMsg;

@property (nonatomic, strong, readwrite)NSNumber *netFail;

@property (nonatomic, strong, readwrite)NSNumber *registerSuccessOrFail;

@end

@implementation RegisterViewModel

- (void)Register {
	if ([[self.username stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] isEqualToString:@""] ||
		[[self.password stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] isEqualToString:@""] ||
		[[self.againPassword stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] isEqualToString:@""] ||
		[[self.realName stringByTrimmingCharactersInSet: [NSCharacterSet whitespaceAndNewlineCharacterSet]] isEqualToString:@""]) {
		self.invalid = @YES;
		self.invalidMsg = @"字段非空";
		return;
	}

	if (![[self.password stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] isEqualToString:[self.againPassword stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]]]) {
		self.invalid = @YES;
		self.invalidMsg = @"两次输入的密码不一致";
		return;
	}

	if (self.username && self.realName && self.apssword) {
		NSDictionary *params = @{@"username":self.username,@"password":self.password,@"realname":self.realName};
		[XDNetworking postWithUrl:API_SIGNUP refreshRequest:YES cache:NO params:params progressBlock:nil successBlock:^(id response) {
			if (response[@"success"] && [response[@"success"] intValue] == 0) {
				self.registerSuccessOrFail = @NO;

				self.invalidMsg = [NSString stringWithFormat:@"%@",response[@"error"]];
			}else {
				UserModel* user = [UserModel alloc]initWithDirectionary:response];

				[[CoreDataManager shareManager] switchToDatabase:[Utils md5:user.username]];

				[[NSUserDefaults standardUserDefaults] setValue:user.uid forKey:UID];
				[[NSUserDefaults standardUserDefaults] setValue:response[@"token"] forKey:TOKEN];

				UserStatusManager *manager = [UserStatusManager shareManager];
				manager.UserModel = user;
				manager.isLogin = @YES;

				self.registerSuccessOrFail = @YES;
			}
		} failBlock:^(NSError *error) {
			self.netFail = @YES;
		}];
	} 	
}

@end
