Component({
  properties: {
    mealType: {
      type: String,
      value: ''
    },
    mealTime: {
      type: String,
      value: ''
    },
    foods: {
      type: Array,
      value: []
    },
    calories: {
      type: Number,
      value: 0
    }
  },
  methods: {
    onTapMeal() {
      this.triggerEvent('tap', {
        mealType: this.properties.mealType,
        mealTime: this.properties.mealTime,
        foods: this.properties.foods,
        calories: this.properties.calories
      })
    }
  }
}) 