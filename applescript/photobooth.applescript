# Take a specified number of photos with a set delay.

set shotsNumber to 4
set delayTime to 2

repeat shotsNumber times
	activate application "EOS Utility"
	tell application "System Events" to tell process "EOS Utility" to keystroke space
	delay delayTime
end repeat