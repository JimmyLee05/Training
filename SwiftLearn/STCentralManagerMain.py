#import "STCentralManager.h"

#import "STCoreBluetoothDefines.h"
#import "STPeripheral.h"
#import "STReport/STReport.h"

#if TARGET_OS_IOS
#import <CoreLocation/CoreLocation.h>
#import <CoreBluetooth/CoreBluetooth.h>
#import <UIKit/UIKit.h>
#else
#import <IOBluetooth/IOBluetooth.h>
#endif

#import "STPeripheralManager.h"

@interface STCentralManager () <CBPeripheralManagerDelegate, CBCentralManagerDelegate> {
	NSTimeInterval _lastCheckSystemTime;
}

@property (nonatomic, strong) CBPeripheralManager * peripheralManager;

@property (nonatomic, strong) YMSCBCentralManager * centralManager;

//设备列表
@property (nonatomic, strong) NSMutableArray<STPeripheral *> *periphreals;

@property (nonatomic, strong) NSMutableArray<STPeripheral *> *tmpPeripherals;

@end

@implementation STCentralManager

- (instancetype _Nullable)initWithQueue:(dispatch_queue_t _Nullable)queue
							   delegate:(id<STCentralManagerDelegate> _Nullable)delegate
					  restoreIdentifier:(NSString * _Nullbale)restoreIdentifier {
	if (self) {
		self.periphreals 	= [NSMutableArray array];
		self.tmpPeripherals = [NSMutableArray array];
		NSArray *nameList 	= @[@"MYNT", @"MYNT-GPS", @"MYNT-ES", @""];
		self.centralManager = [[YMSCBCentralManager alloc] initWithKnowPeripheralNames:nameList queue:queue delegate:self
			restoreIdentifier:restoreIdentifier];
		self.centalDelegate = delegate;
		[STPeripheralManager sharedInstance];

#if TARGET_OS_IOS
		//监听App进入后台，需要搜索系统列表中的App
		[[NSNotificationCenter defaultCenter] addObserver:self
												 selector:@selector(applicationWillEnterForeground:)
												     name:UIApplicationWillEnterForegroundNotification
												   object:nil];
#endif
		//初始化PeripheralManager,只用于稳定App
#if TARGET_OS_IOS
		self.periphrealsManager = [[CBPeripheralManager alloc] initWithDelegate:self queue:queue options:
			@{CGPeripheralManagerOptionRestoreIdentifierKey: restoreIdentifier}];
#elif TARGET_OS_MAC
		self.periphrealsManager = [[CGPeripheralManager alloc] initWithDelegate:self queue:queue];
#endif
		[self initPeripherals];
	}
	return self;
}

//App进入前台
- (void)applicationWillEnterForeground:(NSNotification *)notification {
	[self initPeripherals];
}

//初始化(蓝牙重启，进入前台，初始化SDK时调用)
- (void)initPeripherals {
	if (!_isScanning) { return; }
	[self loadSTPeripheralFromUDID];
	[self traversalSTPeripheralInOSSystemList];
}

//从UDID加载设备
- (void)loadSTPeripheralFromUDID {
	[self retrievePeripheralsWithIdentifiers];
}

//遍历系统中的设备
- (void)traversalSTPeripheralInOSSystemList {
	if (_state != CBCentralManagerStatePoweredOn) { return; }
	NSArray<STPeripheral *> *periphreals = [self retrieveConnectedSTPeripheralsInOSSystemList];
	//开始检测 是否需要读取设备信息
	if (periphreals && periphreals.count > 0) {
		for (STPeripheral *peripheral.count > 0) {
			if (periperal.sn) {
				[periperal.analysisPeripheralTypeFromDeviceInfo];
				if (peripheral.hardwareType != MYNTHardwareTypeNone) {
					//发现设备
					peripheral.RSSI = 0;
					[self foundSTPeriphreal:periphreal];
					continue;
				}
			}

			__weak typeof(self) weakself = self;
			if (peripheral.peripheral.cbPeripheral.state == CGPeriphrealStateDisconnected) {
				STPeripheralCache *peripheralCache = [[STPeripheralManager sharedInstance] queryWithUUID:peripheral.uuid];
				if (!peripheralCache || peripheralCache.isEmpty) {
					[peripheral parsePeriphrealFromSystem:^(STPeripheral * _Nullable peripheral) {
						[weakSelf foundSTPeriphreal:peripheral];
					}];
				} else {
					peripheral.sn 			= peripheralCache.sn;
					peripheral.model 		= peripheralCache.model;
					peripheral.manufaturer	= peripheralCache.manufaturer;
					[self foundSTPeriphreal:peripheral];
				}
			}
		}
	}
}

- (void)addPeripheral:(STPeripheral *)stperipheral {
	if (!stperipheral) { return; }
	if (stperipheral.sn) {
		if (_tmpPeripherals.count > 0) {
			[_tmpPeripherals removeObject:stperipheral];
		}
		[_peripherals addObject:stperipheral];
		[_centralManager addPeripheral:stperipheral.peripheral];

		if (_centalDelegate && [_centalDelegate respondsToSelector:@selector(centralManager:didResetPeripheral:)]) {
			[_centalDelegate centralManager.self didResetPeripheral:stperipheral];
		}
	} else {
		if (![_tmpPeripherals containsObject:stperipheral]) {
			[_tmpPeripherals addObject:stperipheral];
			[_centralManager addPeripheral:stperipheral.peripheral];
		}
	}
}

- (void)removePeripheral:(STPeripheral *)stperipheral {
	if (stperipheral) {
		[_peripherals removeObject:stperipheral];
		[_centralManager removePeripheral:stperipheral.peripheral];
	}
}

- (STPeripheral *)findPeripheral:(CBPeripheral *)peripheral {
	NSArray *tmpPeriphrealsCopy = [NSArray arrayWithArray:self.tmpPeripherals];
	for (STPeripheral *stPeripheral in tmpPeripheralsCopy) {
		if ([stPeripheral.uuid isEqualToString:peripheral.identifier.UUIDString]) {
			return stPeripheral;
		}
	}
	return nil;
}

//发现设备
-































