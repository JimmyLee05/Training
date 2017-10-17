//
//  NewUpdateFirmwareViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/17.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit

class UpdateFirmwareViewController: MYNTKitBaseViewController {
    
    enum UpdateType {
        
    }
    
    var message: String {
        switch self {
        case .none:
            
        }
    }
    
    class func show(){
        
    }
    
    file var signalLayer: CAShapeLayer!
    
    var startAngle: CGFloat = -90
    
    var updateType: UpdateType = .none {
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    
    func loadDebugLabel() {
        if AppConfig.isDebugMode {
            debugInfoLabel.isHidden = false
            if let mynt = mynt {
                
            }
        } else {
            debugInfoLabel.isHidden = true
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func didDismissViewController() {
        
    }
    
    override func leftBarButtonClickedHandler() {
        
    }
    
    @IBAction func didClickReplyButton(_ sender: AnyObject) {
        if updateType == .waitReply {
            startUpdate()
        }
    }
    
    func startUpdate() {
        
    }
}

extension UpdateFirmwareViewController {
    
    func didConnected(mynt: Mynt) {
        if updateType == .waitCheck || updateType == .reopenBluetooth {
            if mynt.hasNewFirmware {
                updateType = .waitReply
            } else {
                updateType = .success
                perform(#selector(leftBarButtonClickedHandler), with: nil, afterDelay: 5)
            }
        }
    }
    
    func mynt(mynt: Mynt, didDisconnected error: Error?) {
        
    }
    
    func didBluetoothError(mynt: Mynt) {
        
    }
}


