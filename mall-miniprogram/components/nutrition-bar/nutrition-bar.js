Component({
  properties: {
    current: {
      type: Number,
      value: 0
    },
    target: {
      type: Number,
      value: 100
    },
    label: {
      type: String,
      value: ''
    },
    showValue: {
      type: Boolean,
      value: true
    },
    color: {
      type: String,
      value: '#1aad19'
    }
  },
  data: {
    percentage: 0
  },
  observers: {
    'current, target': function(current, target) {
      if (target <= 0) {
        this.setData({
          percentage: 0
        })
        return
      }
      let percentage = (current / target) * 100
      percentage = percentage > 100 ? 100 : percentage
      this.setData({
        percentage
      })
    }
  }
}) 