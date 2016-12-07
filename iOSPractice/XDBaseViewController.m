#import "XDBaseViewController.h"

@interface XDBaseViewController ()

@end

@implementation XDBaseViewController

- (void)viewDidLoad {

	[super viewDidLoad];

	[self configureView];

	[self KVOHandler];
}

- (void)KVOHandler{};

- (void)configureView{};

- (void)didReceiveMemoryWarning {
	
	[super didReceiveMemoryWarning];
}

@end