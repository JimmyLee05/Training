//
//  NewMyntRealMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/30.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import SlightechKit

fileprivate class RadiusCircleAnnotation: NSObject, MKAnnotation {
    
    public var coordinate: CLLocationCoordinate2D {
        willSet { willChangeValue(forKey: "coordinate") }
        didSet  { didChangeValue(forKey: "coordinate") }
    }
    
    //火星坐标
    init(coordinate: CLLocationCoordinate2D) {
        self.coordinate = coordinate
    }
}

// 实时定位模块
class NewMyntRealMapViewController: MYNTKitBaseViewController, UIGestureRecognizerDelegate, UIAlertViewDelegate {
    
    @discardableResult
    class func show()
}
