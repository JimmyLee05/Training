//
//  RunController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/27.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import UIKit
import CoreMotion
import AVFoundation
import SCLAlertView

let pedon: CMPedometer = CMPedometer()

@available(iOS 10.0, *)
class RunController: UIViewController {

    static let shared = RunController()

    let CoreData = CoreDataManager.shared
    let fitModel = FitModel.shared

    @IBOutlet weak var distanceLabel: UILabel!
    @IBOutlet weak var speedLabel: UILabel!
    @IBOutlet weak var timeLabel: UILabel!
    @IBOutlet weak var heatLabel: UILabel!

    @IBOutlet weak var startButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    @IBOutlet weak var pauseButton: UIButton!
    @IBOutlet weak var buttonContainer: UIView!
    @IBOutlet weak var closeButton: UIButton!


    var timer: DispatchSourceTimer!
    var second: TimeInterval = 0
    var timeDic: [String: Int]!

    var distanceValue: Double? {
        didSet {
        }
    }

    var isBegin: Bool = false
    var isRunning: Bool = false


    var player: AVPlayer?
    var playerLayer: AVPlayerLayer?

    fileprivate let animationDuration = 0.3

    override func viewDidLoad() {
        super.viewDidLoad()
        
        NotificationCenter.default
            .addObserver(self,
                         selector: #selector(willEnterForeground),
                         name: NSNotification.Name.UIApplicationWillEnterForeground, object: nil)

    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        willEnterForeground()
    }

    override func viewWillDisappear(_ animated: Bool) {

    }

    @objc func willEnterForeground() {
        print("willEnterForeground called from controller")
    }

    @IBAction func clickStartButton(_ sender: Any) {
        startRunning()
    }

    @IBAction func clickStopButton(_ sender: Any) {
        stopRunning()
    }

    @IBAction func togglePaused(_ sender: Any) {
        isRunning ? pauseRunning() : keepRunning()
    }

    @IBAction func didClickCloseButton(_ sender: Any) {
        close()
    }


    override func viewDidAppear(_ animated: Bool) {

    }

    override func viewDidDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}

@available(iOS 10.0, *)
extension RunController {

    func startUpdates(){

        if CMPedometer.isStepCountingAvailable(){

            isRunning = true

            //获取指定开始时间到当前时间的数据参数: 开始时间, 一个闭包
            pedon.startUpdates(from: Date(), withHandler: { (pedometerData, error) in

                if error != nil {
                    print("error:\(String(describing: error))")
                    DispatchQueue.main.async(execute: {
                        print("发生错误")
                    })
                }
                else {
                    DispatchQueue.main.async(execute: {
                        if #available(iOS 9.0, *) {
                            guard pedometerData?.currentPace != nil else {
                                return
                            }
                            //当前配速
                            let currentPace = Float(truncating: (pedometerData?.currentPace)!) * Float(1000/60)
                            let paceDic = self.fitModel.dictionaryFromTimePace(pace: currentPace)
                            self.speedLabel.text = "\(paceDic["m"]!)'\(paceDic["s"]!)''"

                            let distanceInt = Int(truncating: (pedometerData?.distance)!)/100
                            self.fitModel.reportDistance(distance: distanceInt, time: self.second)

                        } else {
                            print("当前系统版本不支持获取配速，正在使用算法估算")
                        }
                        let distanceFloat = String(format: "%.2f", Float(truncating: (pedometerData?.distance)!)/1000)
                        self.distanceLabel.text = distanceFloat
                        let distance = Double(distanceFloat)
                        self.distanceValue = distance
                    })
                }
            })
        }
    }

    //开始运动
    func startRunning(){
        fitModel.reportStatus(status: "start")
        print("开始运动")
        self.startUpdates()
        animateStarted()
        if timer == nil {
            self.timeInterval()
        }
        isBegin = true
    }

    //暂停运动
    func pauseRunning(){
        fitModel.reportStatus(status: "pause")
        print("运动已暂停")
        
        animatePaused()
        //若计时器没有取消，则暂停计时
        if timer?.isCancelled == false {
            timer?.suspend()
        }
        isRunning = false
    }

    //继续运动
    func keepRunning(){
        fitModel.reportStatus(status: "keep")
        animateUnpaused()
        //若计时器没有取消，则继续计时
        if timer?.isCancelled == false {
            timer?.resume()
        }
        isRunning = true
    }

    //停止运动
    func stopRunning(){

        let alertView = SCLAlertView()
        alertView.addButton("结束") {
            self.fitModel.reportStatus(status: "stop")
            self.animateStopped()
            //停止更新
            pedon.stopUpdates()

            if self.timer?.isCancelled == false {
                self.timer?.cancel()
            }
            self.saveRun()
            self.distanceLabel.text = String(format: "%.2f", 0.00)
            self.close()
        }
        let alertViewIcon = UIImage(named: "doubt.png")
        alertView.showNotice("确定结束这次跑步吗?",
                              subTitle: "",
                              closeButtonTitle: "取消",
                              circleIconImage: alertViewIcon)
    }

    //定时器
    func timeInterval(){
        timer = DispatchSource.makeTimerSource(flags: [], queue: DispatchQueue.global())
        timer?.schedule(deadline: .now(), repeating: 1.0)
        timer?.setEventHandler {
            DispatchQueue.main.async(execute: {
                self.timeDic = self.fitModel.dictionaryFromTimeInterval(interval: self.second)
                let timeStr = String(format: "%02d:%02d:%02d", self.timeDic["h"]!, self.timeDic["m"]!, self.timeDic["s"]!)
                self.timeLabel.text = timeStr
                self.second += 1
            })
        }
        timer?.resume()
    }

    private func saveRun() {

        if distanceValue == nil {
            print("no data")
        } else {
            CoreDataManager.shared.saveDistance(distance: distanceValue!)
        }

        print("查看存储的数据 \(String(describing: distanceValue))")
    }

    func close(){
        self.dismiss(animated: true, completion: nil)
    }

    fileprivate func animateStarted() {
        let deltaY: CGFloat = 54
        buttonContainer.frame.origin.y += deltaY
        buttonContainer.isHidden = false

        UIView.animate(withDuration: animationDuration, animations: {
            self.startButton.alpha = 0.0
            self.buttonContainer.alpha = 1.0
            self.buttonContainer.frame.origin.y += -deltaY
        })
    }

    fileprivate func animateStopped() {
        UIView.animate(withDuration: animationDuration, animations: {
            self.startButton.alpha = 1.0
            self.buttonContainer.alpha = 0.0
        })

        pauseButton.setTitle("开始", for: UIControlState())
    }

    fileprivate func animatePaused() {
        pauseButton.setTitle("继续", for: UIControlState())
    }

    fileprivate func animateUnpaused() {
        pauseButton.setTitle("暂停", for: UIControlState())
    }
}
