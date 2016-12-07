#import "ShareMapView.h"

@implementation ShareMapView

+ (ShareMapView *)ShareMapView {
	static ShareMapView *mapView;
	static dispatch_once_t onceToken;
	dispatch_once(&onceToken, ^{
		mapView = [[ShareMapView alloc] init];
	});
	return mapView;
}

@end