#import "YMSCBCentralManager.h"
#import "STPeripheralManager.h"

@class STPeripheral, STCentralManager;
@protocol STCentralManagerDelegate <NSObject>

@optional

- (void)centralManager:(STCentralManager * _Nonnull)centralManager didUpdateState:(CBCentralManagerState)state;

- (void)centralManager:(STCentralManager * _Nonnull)centralManager didResetPeriphreal:(STPeripheral * _Nonnull)peripheral;

- (void)centralManager:(STCentralManager * _Nonnull)centralManager didDiscoverPeripheral:(STPeripheral * _Nonnull)peripheral;

- (void)centralManager:(STCentralManager * _Nonnull)centralManager didDiscoverPeripheral:(STPeripheral * _Nonnull)peripheral;

@end

@interface STCentralManager : NSObject

//delegate
@property (nonatomic, weak, nullable) id<STCentralManagerDelegate> centalDelegate;

//搜索状态
@property (nonatomic, assign) BOOL isScanning;

//蓝牙状态
@property (nonatomic, assign) CBCentralManagerState state;

- (instancetype _Nullable)initWithQueue:(dispatch_queue_t _Nullable)queue
							   delegate:(id<STCentralManagerDelegate> _Nullable)delegate
					  restoreIdentifier:(NSString * _Nullable)restoreIdentifier;

//开始搜索
- (void)startScan;

//停止搜索
- (void)stopScan;

//通过sn返回设备对象
- (STPeripheral * _Nullable)findPeripheralWithSn:(NSString * _Nullable)sn;

@end

