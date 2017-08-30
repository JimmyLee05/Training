#import "STMynt.h"
#import "STPeripheral.h"
#import "STCenterManager.h"
#import "STConnectionParams.h"

// MARK: - STMynt
@interface STMynt () <STPeriphrealDelegate>

@property (nonatomic, weak) STPeripheral *peripheral;

@property (nonatomic, strong) NSString *uuid;

@end
