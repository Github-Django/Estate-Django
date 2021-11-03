const startValue = document.querySelector('.multi-ranges-start-values');
const startValueValues = document.querySelector('#multi-ranges-start-values-show');

const startValueInit = new mdb.MultiRangeSlider(startValue, {
    startValues: [40, 80],
});