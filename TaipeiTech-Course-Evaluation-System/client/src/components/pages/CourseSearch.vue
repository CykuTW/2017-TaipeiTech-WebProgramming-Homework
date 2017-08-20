<template lang="pug">
div#course-search
  el-row
    el-col(:span='20', :offset='2')
      el-collapse(v-model='activeNames')
        el-collapse-item(title='以開課時間查詢', name='1')
          el-form#searchForm1(ref='searchForm1', :model='searchForm1', :rules='searchRules1', label-position="right", label-width="80px")
            el-row
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='學年度', prop='year')
                  el-select(v-model='defaultYearOption', size='large')
                    el-option(
                      v-for='item in yearOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='學期', prop='sem')
                  el-select(v-model='defaultSemOption', size='large')
                    el-option(
                      v-for='item in semOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
            el-row
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='學制(部別)', prop='matric')
                  el-select(v-model='defaultMatricOption', size='large')
                    el-option(
                      v-for='item in matricOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='開課單位', prop='unit')
                  el-select(v-model='defaultUnitOption', size='large')
                    el-option(
                      v-for='item in unitOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
            el-row
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='星期', prop='D')
                  el-select#daySelect(v-model='defaultDayOptions', multiple, placeholder='可複選', size='large', @change='clearDayOptions')
                    el-option(label='全選', value='all')
                    el-option(label='清空', value='clear')
                    el-option(
                      v-for='item in dayOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
              el-col(
                :xs='{span: 24, offset: 0}'
                :sm='{span: 12, offset: 0}'
                :md='{span: 12, offset: 0}'
                :lg='{span: 12, offset: 0}'
              )
                el-form-item(label='節次', prop='P')
                  el-select(v-model='defaultPeriodOptions', multiple, placeholder='可複選', size='large', @change='clearPeriodOptions')
                    el-option(label='全選', value='all')
                    el-option(label='清空', value='clear')
                    el-option(
                      v-for='item in periodOptions',
                      :key='item.value',
                      :label='item.label',
                      :value='item.value'
                    )
            el-form-item(label='課程名稱', v-model='searchForm1.cname', prop='cname')
              el-input(v-model='searchForm1.cname', auto-complete='off')
            el-form-item(label='教師姓名', v-model='searchForm1.tname', prop='tname')
              el-input(v-model='searchForm1.tname', auto-complete='off')
            el-form-item
              el-button(type='primary', @click="submitForm('searchForm1')") 查詢
              el-button(@click="resetForm('searchForm1')") 清除
        el-collapse-item(title='以課程概述查詢', name='2')
          el-form#searchForm2(ref='searchForm2', :model='searchForm2', :rules='searchRules2', label-position="right", label-width="80px")
            el-form-item(label='課程名稱', prop='cname')
              el-input(v-model='searchForm2.cname', auto-complete='off')
            el-form-item(label='課程編號', prop='ccode')
              el-input(v-model='searchForm2.ccode', auto-complete='off')
            el-form-item
              el-button(type='primary', @click="submitForm('searchForm2')") 查詢
              el-button(@click="resetForm('searchForm2')") 清除
      br
      component(:is='tableComponent', :data='tableData', :loading='loading')
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'
import SearchTable1 from '@/components/SearchTable1'
import SearchTable2 from '@/components/SearchTable2'

export default {
  name: 'CurseSearch',
  components: {
    SearchTable1,
    SearchTable2
  },
  computed: mapGetters([
    'api'
  ]),
  data() {
    return {
      searchForm1: {
        cname: '程式',
        tname: ''
      },
      searchRules1: {
      },
      searchForm2: {
        cname: '',
        ccode: ''
      },
      searchRules2: {
      },
      tableComponent: SearchTable1,
      tableData: [
      ],
      yearOptions: [
        {
          value: 106,
          label: '106 學年度'
        }
      ],
      semOptions: [
        {
          value: 1,
          label: '上學期'
        },
        {
          value: 2,
          label: '下學期'
        }
      ],
      dayOptions: [
        { value: 1, label: '一' },
        { value: 2, label: '二' },
        { value: 3, label: '三' },
        { value: 4, label: '四' },
        { value: 5, label: '五' },
        { value: 6, label: '六' },
        { value: 7, label: '日' }
      ],
      periodOptions: [
        { value: 1, label: '1'},
        { value: 2, label: '2'},
        { value: 3, label: '3'},
        { value: 4, label: '4'},
        { value: 5, label: '5'},
        { value: 6, label: '6'},
        { value: 7, label: '7'},
        { value: 8, label: '8'},
        { value: 9, label: '9'},
        { value: 10, label: 'A'},
        { value: 11, label: 'B'},
        { value: 12, label: 'C'},
        { value: 13, label: 'D'}
      ],
      matricOptions: [
        { value: "'0','1','4','5','6','7','8','9','A','C','D','E','F'", label: "全校" },
        { value: "'1','5','6','7','8','9'", label: "日間部" },
        { value: "'7'", label: "日間部四技" },
        { value: "'8','9'", label: "日間部研究所(碩、博)" },
        { value: "'4','A','D','C','E','F'", label: "進修部" },
        { value: "'4'", label: "進修部二技" },
        { value: "'E'", label: "學士後學位學程" },
        { value: "'F'", label: "進修部四技" },
        { value: "'A'", label: "進修部碩士在職專班" },
        { value: "'D'", label: "ＥＭＢＡ" },
        { value: "'C'", label: "週末碩士班" },
        { value: "'8','9','A','C','D'", label: "研究所(日間部、進修部、週末碩士班)" },
        { value: "'0'", label: "進修學院(二技)" },
        { value: "'0','4','6'", label: "二技(日間部、進修部暨進修學院)" },
        { value: "'7','F'", label: "四技(日間部、進修部)" },
        { value: "'1'", label: "學程" }
      ],
      unitOptions: [
        { value: "**", label: "所有系所" },
        { value: "01", label: "教務處" },
        { value: "05", label: "進修部" },
        { value: "06", label: "進修學院" },
        { value: "10", label: "體育室" },
        { value: "14", label: "通識教育中心" },
        { value: "30", label: "機械工程系" },
        { value: "31", label: "電機工程系" },
        { value: "32", label: "化學工程與生物科技系" },
        { value: "33", label: "材料及資源工程系" },
        { value: "34", label: "土木工程系" },
        { value: "35", label: "分子科學與工程系" },
        { value: "36", label: "電子工程系" },
        { value: "37", label: "工業工程與管理系" },
        { value: "38", label: "工業設計系" },
        { value: "39", label: "建築系" },
        { value: "40", label: "機電整合研究所" },
        { value: "41", label: "電腦與通訊研究所" },
        { value: "42", label: "土木與防災研究所" },
        { value: "44", label: "車輛工程系" },
        { value: "45", label: "能源與冷凍空調工程系" },
        { value: "49", label: "技術及職業教育研究所" },
        { value: "51", label: "有機高分子研究所" },
        { value: "52", label: "建築與都市設計研究所" },
        { value: "54", label: "應用英文系" },
        { value: "56", label: "製造科技研究所" },
        { value: "57", label: "經營管理系" },
        { value: "58", label: "創新設計研究所" },
        { value: "59", label: "資訊工程系" },
        { value: "60", label: "環境工程與管理研究所" },
        { value: "61", label: "自動化科技研究所" },
        { value: "62", label: "師資培育中心" },
        { value: "63", label: "光電科技中心" },
        { value: "64", label: "自動化科技中心" },
        { value: "65", label: "光電工程系" },
        { value: "66", label: "機電科技研究所" },
        { value: "67", label: "工程科技研究所" },
        { value: "68", label: "生化與生醫工程研究所" },
        { value: "73", label: "化學工程研究所" },
        { value: "74", label: "工商管理研究所" },
        { value: "76", label: "軟體工程學程" },
        { value: "78", label: "材料科學與工程研究所" },
        { value: "79", label: "資源工程研究所" },
        { value: "81", label: "機電學士班" },
        { value: "82", label: "電資學士班" },
        { value: "83", label: "工程科技學士班" },
        { value: "84", label: "創意設計學士班" },
        { value: "85", label: "設計研究所" },
        { value: "86", label: "電資碩士在職專班" },
        { value: "91", label: "科技法律學程" },
        { value: "92", label: "互動媒體設計研究所" },
        { value: "93", label: "資訊與運籌管理研究所" },
        { value: "98", label: "管理學院外國學生專班" },
        { value: "99", label: "電資學院外國學生專班" },
        { value: "A0", label: "工程學院能源與光電材料外國學生專班" },
        { value: "A1", label: "服務與科技管理研究所" },
        { value: "A4", label: "智慧財產權研究所" },
        { value: "A5", label: "文化事業發展系" },
        { value: "A6", label: "設計學院創意與永續建築研究所外國學生專班" },
        { value: "A8", label: "機電科技研究所外國學生專班" },
        { value: "A9", label: "工程學院土木與環境工程外國學生專班" },
        { value: "AA", label: "校院級課程" },
        { value: "AB", label: "資訊與財金管理系" },
        { value: "AC", label: "互動設計系" },
        { value: "C2", label: "管理學院" }
      ],
      defaultDayOptions: [
        1, 2, 3, 4, 5, 6, 7
      ],
      defaultPeriodOptions: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
      ],
      defaultMatricOption: "'0','1','4','5','6','7','8','9','A','C','D','E','F'",
      defaultUnitOption: "**",
      defaultYearOption: 106,
      defaultSemOption: 1,
      activeNames: ['1'],
      loading: false
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (formName === 'searchForm1')
            this.submitSearch1();
          else if (formName === 'searchForm2')
            this.submitSearch2();
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    submitSearch1() {
      this.loading = true;
      this.tableData = [];
      this.tableComponent = SearchTable1;

      let data = '?';
      data += '&cname=' + encodeURIComponent(this.searchForm1.cname);
      data += '&tname=' + encodeURIComponent(this.searchForm1.tname);
      data += '&matric=' + encodeURIComponent(this.defaultMatricOption);
      data += '&unit=' + encodeURIComponent(this.defaultUnitOption);
      data += '&year=' + encodeURIComponent(this.defaultYearOption.toString());
      data += '&sem=' + encodeURIComponent(this.defaultSemOption.toString());
      this.defaultDayOptions.forEach((option) => {
        data += '&D[]=' + encodeURIComponent(option.toString());
      });
      this.defaultPeriodOptions.forEach((option) => {
        data += '&P[]=' + encodeURIComponent(option.toString());
      });

      fetch(this.api.course.search1 + data, {
        credentials: "include",
        method: 'GET',
        headers: {
          'Content-Type':'application/x-www-form-urlencoded'
        }
      }).then((response) => {
        return response.json();
      }).then((json) => {
        this.tableData = json.courses;
        this.loading = false;
        console.log(json);
      }).catch((error) => {
        console.log(error);
      });
    },
    submitSearch2() {
      this.loading = true;
      this.tableData = [];
      this.tableComponent = SearchTable2;

      let data = '?';
      data += '&cname=' + encodeURIComponent(this.searchForm2.cname);
      data += '&ccode=' + encodeURIComponent(this.searchForm2.ccode);

      fetch(this.api.course.search2 + data, {
        credentials: "include",
        method: 'GET',
        headers: {
          'Content-Type':'application/x-www-form-urlencoded'
        }
      }).then((response) => {
        return response.json();
      }).then((json) => {
        this.tableData = json.courses;
        this.loading = false;
        console.log(json);
      }).catch((error) => {
        console.log(error);
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    clearDayOptions(values) {
      if (values.indexOf('clear') != -1)
        this.defaultDayOptions = [];
      else if (values.indexOf('all') != -1)
        this.defaultDayOptions = [1, 2, 3, 4, 5, 6, 7];
      else {
        let buffer = values.slice();
        let check = true;
        buffer.sort((a, b) => a-b);
        values.forEach((value, i) => {
          check = value === buffer[i]
        });
        if (!check) {
          this.defaultDayOptions = buffer.slice();
        }
      }
    },
    clearPeriodOptions(values) {
      if (values.indexOf('clear') != -1)
        this.defaultPeriodOptions = [];
      else if (values.indexOf('all') != -1)
        this.defaultPeriodOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];
      else {
        let buffer = values.slice();
        let check = true;
        buffer.sort((a, b) => a-b);
        values.forEach((value, i) => {
          check = value === buffer[i]
        });
        if (!check) {
          this.defaultPeriodOptions = buffer.slice();
        }
      }
    }
  }
}
</script>

<style lang="css">
#course-search {
  margin-top: 3rem;
}

.cell {
  white-space: pre-line !important;
}

</style>
