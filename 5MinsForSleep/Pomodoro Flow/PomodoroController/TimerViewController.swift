//
//  TimerViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit
import AVFoundation
import SCLAlertView

@available(iOS 10.0, *)
class TimerViewController: UIViewController {

    @IBOutlet weak var startButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    @IBOutlet weak var pauseButton: UIButton!
    @IBOutlet weak var buttonContainer: UIView!
    @IBOutlet weak var collectionView: UICollectionView!
    @IBOutlet weak var videoView: UIView!
    @IBOutlet weak var closeButton: UIButton!

    @IBOutlet weak var timerLabel: UILabel!

    var player: AVPlayer?
    var playerLayer: AVPlayerLayer?

    let notificationName = "XMNotification"

    // 单例
    fileprivate let scheduler: Scheduler
    fileprivate let pomodoro    = Pomodoro.shared
    fileprivate let bgMusic     = BgMusicViewController.shared
    fileprivate let fitModel    = FitModel.shared

    // 时间
    fileprivate var timer: Timer?
    fileprivate var currentTime: Double!
    fileprivate var running = false

    fileprivate let animationDuration = 0.3
    fileprivate let settings = SettingsManager.shared

    fileprivate struct CollectionViewIdentifiers {
        static let emptyCell = "EmptyCell"
        static let filledCell = "FilledCell"
    }

    // Pomodoros view
    fileprivate var pomodorosCompleted: Int!
    fileprivate var targetPomodoros: Int

    // MARK: - Initialization
    required init?(coder aDecoder: NSCoder) {
        targetPomodoros = settings.targetPomodoros
        pomodorosCompleted = pomodoro.pomodorosCompleted
        scheduler = Scheduler()

        super.init(coder: aDecoder)
    }

    deinit {
        NotificationCenter.default.removeObserver(self)
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        NotificationCenter.default.addObserver(self,
                                               selector: #selector(willEnterForeground),
                                               name: NSNotification.Name.UIApplicationWillEnterForeground,
                                               object: nil)

        NotificationCenter.default.addObserver(self,
                                               selector: #selector(presentAlertFromNotification(_:)),
                                               name: NSNotification.Name(rawValue: notificationName),
                                               object: nil)


        playVideo()
        bgMusic.playBgMusic()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        willEnterForeground()
    }

    // 进入后台前的设置
    @objc func willEnterForeground() {
        print("willEnterForeground called from controller")

        setCurrentTime()
        updateTimerLabel()
        startVideo()

        if scheduler.pausedTime != nil {
            //Button从下往上的一个动画
            animateStarted()
            animatePaused()
        }
        reloadData()
    }

    @objc func secondPassed() {
        if currentTime > 0 {
            currentTime = currentTime - 1.0
            updateTimerLabel()
            return
        }
        print("State: \(pomodoro.state), done: \(pomodoro.pomodorosCompleted)")

        if pomodoro.state == .default {
            pomodoro.completePomodoro()
            reloadData()
        } else {
            pomodoro.completeBreak()
            reloadData()
        }

        stop()
        startTimer()
        print("State: \(pomodoro.state), done: \(pomodoro.pomodorosCompleted)")
    }

    // MARK: - Actions
    @IBAction func togglePaused(_ sender: EmptyRoundedButton) {
        scheduler.paused ? timerUnpause() : timerPause()
    }

    @IBAction func start(_ sender: RoundedButton) {
        startTimer()
    }

    @IBAction func stop(_ sender: RoundedButton) {
        stopTimer()
    }

    func close() {
        self.dismiss(animated: true, completion: nil)
    }

    @IBAction func clickCloseButton(_ sender: Any) {
        close()
    }
}

// TimerViewController里的一些函数放在拓展里，主控制器可以直接调用
@available(iOS 10.0, *)
extension TimerViewController {

    func startTimer() {
        fitModel.reportStatus(status: "start")
        scheduler.timeStart()
        running = true
        animateStarted()
        fireTimer()
        bgMusic.startBGMusic()
        startVideo()
    }

    func stopTimer() {

        let alertView = SCLAlertView()
        alertView.addButton("结束") {
            self.fitModel.reportStatus(status: "stop")
            self.scheduler.timeStop()
            self.running = false
            self.animateStopped()
            self.timer?.invalidate()
            self.resetCurrentTime()
            self.updateTimerLabel()
            self.bgMusic.stopBGMusic()
            self.stopVideo()
            self.close()
        }
        let alertViewIcon = UIImage(named: "doubt.png")
        alertView.showNotice("确定结束这次运动吗?",
                              subTitle: "",
                              closeButtonTitle: "取消",
                              circleIconImage: alertViewIcon)
    }

    func stop() {
        scheduler.timeStop()
        running = false
        animateStopped()
        timer?.invalidate()
        resetCurrentTime()
        updateTimerLabel()
    }

    func timerPause() {
        fitModel.reportStatus(status: "pause")
        guard running else { return }

        scheduler.timePause(currentTime)
        running = false
        timer?.invalidate()
        animatePaused()
        bgMusic.stopBGMusic()
        stopVideo()
    }

    func timerUnpause() {
        fitModel.reportStatus(status: "keep")
        scheduler.timeUnpause()
        running = true
        fireTimer()
        animateUnpaused()
        bgMusic.startBGMusic()
        startVideo()
    }

    @objc func presentAlertFromNotification(_ notification: Notification) {

        guard let notification = notification.object as? UILocalNotification else {
            return
        }
        
        let alertController = UIAlertController(title: notification.alertTitle,
                                                message: notification.alertBody,
                                                preferredStyle: .alert)

        let okAction = UIAlertAction(title: "OK", style: .default) { action in print("OK") }
        alertController.addAction(okAction)

        present(alertController, animated: true, completion: nil)
        print("弹出选择框")
    }
    
    // MARK: - Helpers
    fileprivate func reloadData() {
        targetPomodoros = settings.targetPomodoros
        pomodorosCompleted = pomodoro.pomodorosCompleted
        collectionView.reloadData()
    }

    fileprivate func updateTimerLabel() {
        let time = Int(currentTime)
        timerLabel.text = String(format: "%02d:%02d", time / 60, time % 60)
    }

    fileprivate func setCurrentTime() {
        if let pausedTime = scheduler.pausedTime {
            currentTime = pausedTime
            return
        }
        if let fireDate = scheduler.fireDate {
            let newTime = fireDate.timeIntervalSinceNow
            currentTime = (newTime > 0 ? newTime : 0)
            return
        }
        resetCurrentTime()
    }

    fileprivate func resetCurrentTime() {
        switch pomodoro.state {
        case .default: currentTime = Double(settings.pomodoroLength)
        case .shortBreak: currentTime = Double(settings.shortBreakLength)
        case .longBreak: currentTime = Double(settings.longBreakLength)
        }
        resetTimerLabelColor()
    }

    fileprivate func resetTimerLabelColor() {
        switch pomodoro.state {
        case .default: timerLabel.textColor = UIColor.accentColor
        case .shortBreak, .longBreak: timerLabel.textColor = UIColor.breakColor
        }
    }

    fileprivate func fireTimer() {
        timer = Timer.scheduledTimer(timeInterval: 1,
                                     target: self, selector: #selector(secondPassed), userInfo: nil, repeats: true)
    }

    fileprivate func refreshPomodoros() {
        targetPomodoros = settings.targetPomodoros
        collectionView.reloadData()
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

        pauseButton.setTitle("暂停", for: UIControlState())
    }

    fileprivate func animatePaused() {
        pauseButton.setTitle("继续", for: UIControlState())
    }

    fileprivate func animateUnpaused() {
        pauseButton.setTitle("暂停", for: UIControlState())
    }
}

@available(iOS 10.0, *)
extension TimerViewController: UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {

    // MARK: UICollectionViewDataSource
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return numberOfSections
    }

    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int {
        return numberOfRows(inSection: section)
    }

    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {

        let index = rowsPerSection * indexPath.section + indexPath.row
        let identifier = (index < pomodorosCompleted!) ?
            CollectionViewIdentifiers.filledCell : CollectionViewIdentifiers.emptyCell

        return collectionView.dequeueReusableCell(withReuseIdentifier: identifier,
                                                  for: indexPath)
    }

    // MARK: UICollectionViewDelegate
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        let bottomInset: CGFloat = 12
        return UIEdgeInsetsMake(0, 0, bottomInset, 0)
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 10.0
    }

    // MARK: Helpers
    fileprivate var rowsPerSection: Int {
        let cellWidth: CGFloat = 30.0
        let margin: CGFloat = 10.0
        return Int(collectionView.frame.width / (cellWidth + margin))
    }

    fileprivate func numberOfRows(inSection section: Int) -> Int {
        if section == lastSectionIndex {
            return numberOfRowsInLastSection
        } else {
            return rowsPerSection
        }
    }

    fileprivate var numberOfRowsInLastSection: Int {
        if targetPomodoros % rowsPerSection == 0 {
            return rowsPerSection
        } else {
            return targetPomodoros % rowsPerSection
        }
    }

    fileprivate var numberOfSections: Int {
        return Int(ceil(Double(targetPomodoros) / Double(rowsPerSection)))
    }

    fileprivate var lastSectionIndex: Int {
        if numberOfSections == 0 {
            return 0
        }
        return numberOfSections - 1
    }
}

@available(iOS 10.0, *)
extension TimerViewController {

    func playVideo() {

        let filePath        = Bundle.main.path(forResource: "bodyweight_fitness_diamond_pushup", ofType: ".mp4")
        let videoURL        = NSURL(fileURLWithPath: filePath!)
        let player          = AVPlayer(url: videoURL as URL)

        let playerLayer     = AVPlayerLayer(player: player)
        playerLayer.frame   = videoView.bounds
        playerLayer.videoGravity = AVLayerVideoGravity.resizeAspectFill
        self.videoView.layer.insertSublayer(playerLayer, at: 0)

        self.player = player

        NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime,
                                               object: player.currentItem,
                                               queue: .main) { _ in
                                                self.player?.seek(to: kCMTimeZero)
                                                self.player?.play()
        }
    }

    func startVideo() {
        self.player!.play()
    }

    func stopVideo() {
        self.player!.pause()
    }
}

