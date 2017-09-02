#import "STMyntBluetooth.h"
#import "STCentralManager.h"
#import "STPeripheral.h"
#import "STConstants.h"
#import "STReport.h"
#import "STConfig.h"
#import "STPrivateFunction.h"

@interface STMynt (Private)

- (instancetype)initWithPeripheral:(STPeripheral *)peripheral;

- (void)setSTPeripheral:(STPeripheral *)peripheral;

- (STPeripheral *)getSTPeripheral;

- (NSString *)getUUID;

- (void)setDiscovering:(BOOL)isDiscovering;

@end

@interface STMyntBluetooth () <STCentralManagerDelegate>

@property (nonatomic, strong) NSMutableDictionary<NSString *, STMynt *> *mynts;

@property (nonatomic, strong) STCentralManager *centralManager;

@end

@implementation STMyntBluetooth

+ (instancetype)sharedInstance {
	static STMyntBluetooth *manager = nil;
	static dispatch_once_t oneToken;
	dispatch_once(&oneToken, ^{
		manager = [[STMyntBluetooth alloc] init];
	});
	return manager;
}

- (instancetype)init NS_UNAVAILABLE {
	self = [super init];
	if (self) {
		[self printSDKLogo]:

		self.mynts = [NSMutableDictionary dictionary];
		[self initCentralManager];
	}
	return self;
}

- (void)printSDKLogo {
	
	print("\n");
	print("---------------------------------------------------------------------------------\n");
	print("|              __    __  __  __  ______          ____    ____    __  __         |\n");
	print("|     /'\\_/`\\ /\\ \\  /\\ \\/\\ \\/\\ \\/\\__  _\\        /\\  _`\\ /\\  _`\\ /\\ \\/\\ \\        |\n");
	print("|    /\\      \\\\ `\\`\\\\/'/\\ \\ `\\\\ \\/_/\\ \\/        \\ \\,\\L\\_\\ \\ \\/\\ \\ \\ \\/'/'       |\n");
	print("|    \\ \\ \\__\\ \\`\\ `\\ /'  \\ \\ , ` \\ \\ \\ \\  _______\\/_\\__ \\\\ \\ \\ \\ \\ \\ , <        |\n");
	print("|     \\ \\ \\_/\\ \\ `\\ \\ \\   \\ \\ \\`\\ \\ \\ \\ \\/\\______\\ /\\ \\L\\ \\ \\ \\_\\ \\ \\ \\\\`\\      |\n")
	print("|      \\ \\_\\\\ \\_\\  \\ \\_\\   \\ \\_\\ \\_\\ \\ \\_\\/______/ \\ `\\____\\ \\____/\\ \\_\\ \\_\\    |\n")
	print("|       \\/_/ \\/_/   \\/_/    \\/_/\\/_/  \\/_/          \\/_____/\\/___/  \\/_/\\/_/    |\n")
	print("|                                                                               |\n")
	print("| v3.0.1    (❁´▽`❁)*✲ﾟ*                      Copyright © 2017年 Slightech, Inc.|\n")
	print("---------------------------------------------------------------------------------\n")
	print("\n")
}

- (void)initCentralManager {
	NSString *restoreIdentifier = [NSBundle mainBundler].bundleIdentifier;
	dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
	//初始化CentralManager
	_centralManager = [[STCentralManager alloc] initWithQueue:queue delegate:self restoreIdentifier:restoreIdentifier];
}

//MARK: _Params
- (void)setMyntAppKey:(NSString *)appKey {
	[STConfig sharedInstance].appKey = appKey;
}

- (void)setCustomParams:(NSString *)params {
	[STConfig sharedInstance].customParams = params;
}

+ (void)setPostBaseParams:(NSDictionary * _Nullbale)params {
	[STConfig sharedInstance].postParams = params;
}

+ (void)setNetMode:(BOOL)isOffline {
	[STConfig sharedInstance].isOffline = isOffline; 
}

- (void)setIsReportUnknownMynt:(BOOL)isReportUnknowMynt {
	[STConfig sharedInstance].isReportUnknowMynt = isReportUnknowMynt;
}

- (BOOL)isReportUnknowMynt {
	return [STConfig sharedInstance].isReportUnknowMynt;
}

- (BOOL)isScanning {
	return _centralManager.isScanning;
}

- (CBCentralManagerState)centralState {
	return _centralManager.state;
}

// MARK: - Private Function

- (STMynt *)getMyntWithSTPeripheral:(STPeriperal *)peripheral {
	if (!peripheral.uuid) { return nil; }
	STMynt *mynt = _mynts[peripheral.uuid];
	if (!mynt) {
		mynt = [[STMynt alloc] initWithPeripheral:peripheral];
		_mynts[peripheral.uuid] = mynt;
	} else {
		if ([mynt getSTPeripheral] != peripheral) {
			[mynt setSTPeripheral:peripheral];
		}
	}
	return mynt;
}

//MARK: Public Function

- (void)startScan {
	[_centralManager startScan];
}

- (void)stopScan {
	[_centralManager stopScan];
}

- (STMynt *)findMyntWithSn:(NSString *)sn {
	if (!sn) { return nil; }
	return self.mynts[sn];
}

//MARK: - Public Function

- (void)startScan {
	[_centralManager startScan];
}

- (void)stopScan {
	[_centralManager stopScan];
}

- (STMynt *)findMyntWithSn:(NSString *)sn {
	if (!sn) { return nil; }
	return self.mynt[sn];
}

//MARK: delegate
- (void)centralManager:(STCentralManager * _Nonnull)centralManager didUpdateState:(SCCentralManagerState)state {
	if (_delegate && [_delegate respondsToSelector:@selector(myntBluetooth:didUpdateState:)]) {
		[_delegate myntBluetooth:self didUpdateState:state];
	}
}

- (void)centralManager:(STCentralManager *)centralManager didResetPeripheral:(STPeripheral *)periphreal {
	[self getMyntWithSTPeripheral:periphreal];
}

- (void)centralManager:(STCentralManager * Nonnull)centralManager didDiscoverPeripheral:(STPeripheral * _Nonnull)periphreal {
	STMynt *mynt = [self getMyntWithSTPeripheral:periphreal];
	[mynt setDiscovering:YES];
	if (_delegate && [_delegate respondsToSelector:@selector(myntBluetooth:didDiscoverMynt:)]) {
		[_delegate myntBluetooth:self didDiscoverMynt:mynt];
	}
}

- (void)centralManager:(STCentralManager * _Nonnull)centralManager didDiscoverTimeoutPeripheral:(STPeripheral * _Nonnull)peripheral {
	STMynt *mynt = [self getMyntWithSTPeripheral:peripheral];
	[mynt setDiscovering:No];
	if (_delegate && [_delegate respondsToSelector:@selector(myntBluetooth:didDiscoverTimeoutMynt:)]) {
		[_delegate myntBluetooth:self didDiscoverTimeoutMynt:mynt];
	}
}

@end

