//
//  AppUIInitProcess.h
//  CoolRun
//
//  Created by 南君 李 on 2016/12/2.
//  Copyright © 2016年 南君 李. All rights reserved.
//

#import "AppUIInitProcess.h"

static NSString* SELECTVC = @"SelectViewController";

static NSString* FIRSTVC = @"HomeViewController";

@interface AppUIInitProcess()

@property(nonatomic, strong)UIViewController* selectViewController;

@property(nonatomic, strong)UIViewController* firstViewController;

@end

@implementation AppUIInitProcess

- (instancetype)initWithApplication:(UIApplication *)application andLanuchOption:(NSDictionary *)option{
	if (self = [super init]){
		[self initUIWithApplication:application];
	}
	return self;
}

- (void)initUIWithApplication:(UIApplication*)application{
	[AMapLocationServices sharedServices].apiKey =@"1ad2f773b7d4c6dfeab95f79b9242811";
	application.delegate.window = [[UIWindow alloc]initWithFrame:[UIScreen mainScreen].bounds];
	application.delegate.window.rootViewController = self.drawController;

	self.drawController.leftViewController = self.selectViewController;
	self.drawController.centerViewController = self.firstViewController;
	self.drawController.leftDrawerWidth = WIDTH/2;
	self.drawController.animator = self.drawerAnimator;
	self.drawController.backgroundImage = [UIImage imageNamed:@"run.jpg"];
	UIView* backView = [[UIView alloc]initWithFrame:CGRectMake(0, 0, WIDTH, HEIGHT)];
	backView.alpha = 0.5;
	[self.drawController.view insertSubview:backView atIndex:1];

	UserStatusManager *userManager = [UserStatusManager shareManager];

	if ([userManager.isLogin boolValue]) {
		[[CoreDataManager shareManager] switchToDatabase:[Utils md5:userManager.userModle.username]];
	}else {
		[[CoreDataManager shareManager] switchToTempDatabase];
	}

	[application.delegate.window makeKeyAndVisible];

}

-(void)toggleLeftDrawer:(id)sender animated:(BOOL)animated {
	[self.drawController toggleDrawerWithSide:JVFloatingDrawerSideLeft animated:animated completion:nil];
}

#pragma mark - getter and setter 
- (JVFloatingDrawerViweController *)drawController{
	if (!_drawController) {
		_drawController = [[JVFloatingDrawerViweController alloc]init];
	}
	return _drawController;
}

- (JVFloatingDrawerSpringAnimator *)drawerAnimator{
	if (!_drawerAnimator) {
		_drawerAnimator = [[JVFloatingDrawerSpringAnimator alloc]init];
	}
	return _drawerAnimator;
}

- (UIStoryboard *)mainStoryboard{
	if (!_mainStoryboard) {
		_mainStoryboard = [UIStoryboard storyboardWithName:@"Main" bundle:nil];		
	}
	return _mainStoryboard;
}

- (UIViewController *)selectViewController{
	if (!_selectViewController) {
		_selectViewController = [self.mainStoryboard instantiateViewControllerWithIdentifier:SELECTVC];
	}
	return _selectViewController;
}

- (UIViewController *)firstViewController{
	if (!_firstViewController) {
		_firstViewController = [self.mainStoryboard instantiateViewControllerWithIdentifier:FIRSTVC];
	}
	return _firstViewController
}

end