#import "IMNoDataView.h"

@inteface IMNoDataView ()

@property (weak, nonatimic) IBOutlet UILabel *messageLabel;

@end

@implementation IMNoDataView

- (void)awakeFromNib {
	[super awakeFromNib];
	_messageLabel.text = NSLocalizedString(@"IM_NODATA_MESSAGE", @"");
}

@end