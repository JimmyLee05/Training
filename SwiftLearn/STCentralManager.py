#import "YMSCBCentralManager.h"
#import "STPeripheralManager.h"

@class STPeripheral, STCentralManager;
@protocol STCentralManagerDelegate <NSObject>

@optional

- (void)centralManager:()