//
//  SportViewButtons.swift
//  myForm
//
//  Created by bb on 2017/6/1.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit

class SportView: UIView {

    var labelGroupView:UIView!
    var runningInfoView:RunningInfoView!
    
    var buttonGroupView:UIView!
    var controllButtonView:ControllButtonView!
    
    var array = [["imageName":"icon_run_speed_monitor", "titleName":"分钟/公里"], ["imageName":"icon_run_time", "titleName":"用时"], ["imageName":"icon_run_kcal", "titleName":"千卡"]]

    override init(frame: CGRect) {
        super.init(frame: frame)

        labelGroupView = UIView()
        labelGroupView.frame = CGRect(x: 0, y: 0, width: self.bounds.size.width, height: self.bounds.size.height*2/5 - 20)
        //labelGroupView.backgroundColor = UIColor.red
        self.addSubview(labelGroupView)
        
        
        buttonGroupView = UIView()
        buttonGroupView.frame = CGRect(x: 0, y: self.bounds.size.height*2/5 - 20, width: self.bounds.size.width, height: self.bounds.size.height*3/5 + 20)
        //buttonGroupView.backgroundColor = UIColor.yellow
        self.addSubview(buttonGroupView)
        
        for i in 0...2{
            
            //运动信息
            runningInfoView = RunningInfoView(frame: CGRect(x: labelGroupView.bounds.size.width*CGFloat(i)/3, y: 0, width: labelGroupView.bounds.size.width/3, height: labelGroupView.bounds.size.height))
            runningInfoView.title.text = array[i]["titleName"]
            runningInfoView.image.image = UIImage(named: array[i]["imageName"]!)
            labelGroupView.addSubview(runningInfoView)
            switch i {
            case 0:
                runningInfoView.number.text = "--"
                runningInfoView.tag = 1000
                break
            case 1:
                runningInfoView.number.text = "00:00:00"
                runningInfoView.tag = 1001
                break
            case 2:
                runningInfoView.number.text = "0"
                runningInfoView.tag = 1002
                break
            default:
                break
            }
            
            //开始／暂停／结束／继续
            controllButtonView = ControllButtonView(frame: CGRect(x: 0, y: 0, width: buttonGroupView.bounds.size.width/4, height: buttonGroupView.bounds.size.width/4))
            controllButtonView.center.x = buttonGroupView.bounds.size.width/2
            controllButtonView.center.y = buttonGroupView.bounds.size.height/2
            switch i {
            case 0:
                controllButtonView.button.setBackgroundImage(imageMainColor, for: .normal)
                controllButtonView.button.setBackgroundImage(imageMainColor, for: .highlighted)
                controllButtonView.button.setTitle("继续 ", for: .normal)
                controllButtonView.tag = 1003
                controllButtonView.isHidden = true
                controllButtonView.alpha = 0
                controllButtonView.circleView.strokeColor = MainColor
                break
            case 1:
                controllButtonView.button.setBackgroundImage(stopImage, for: .normal)
                controllButtonView.button.setBackgroundImage(stopImage, for: .highlighted)
                controllButtonView.button.setTitle("结束", for: .normal)
                controllButtonView.tag = 1005
                controllButtonView.isHidden = true
                controllButtonView.alpha = 0
                controllButtonView.circleView.strokeColor = UIColor.clear
                break
            case 2:
                controllButtonView.button.setBackgroundImage(imageMainColor, for: .normal)
                controllButtonView.button.setBackgroundImage(imageMainColor, for: .highlighted)
                controllButtonView.button.setTitle("开始", for: .normal)
                controllButtonView.tag = 1004
                controllButtonView.circleView.strokeColor = MainColor
                break
            default:
                break
            }
            
            buttonGroupView.addSubview(controllButtonView)
        }

          
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

}
