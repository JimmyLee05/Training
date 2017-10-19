//
//  NewMyntInfoPresenter.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/19.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation
import SlightextKit

extension MyntInfoViewController {
    
    func initData() {
        if mynt?.myntType == .myntGPS {
            mynt?.downloadActivityInfo(failure: { _, _ in })
            mynt?.simcardStatus(failure: { _, _ in })
        }
        mynt?.downLastLocation()
        contentView?.uiState ?= mynt?.uiState
    }
    
    func didStartConnect(mynt: Mynt) {
        if mynt.sn != self.mynt?.sn { return }
        contentView?.uiState = mynt.uiState
    }
    
    func didConnected(mynt: Mynt) {
        if mynt.sn != self.mynt?.sn { return }
        contentView?.uiState = mynt.uiState
    }
    
    func mynt(mynt: Mynt, didDisconnected error: Error?) {
        if mynt.sn != self.mynt?.sn { return }
        contentView?.uiState = mynt.uiState
    }
    
    func mynt(mynt: Mynt, didUpdateProperty name: String, oldValue: Any?, newValue: Any?) {
        
    }
}
