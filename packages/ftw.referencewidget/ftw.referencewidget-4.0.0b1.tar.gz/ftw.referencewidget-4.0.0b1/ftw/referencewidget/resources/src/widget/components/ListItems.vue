<template>
  <ul class="list-group">
    <template v-for="item in items" :key="item.UID">
      <li class="list-group-item">
        <div class="form-check">
          <input
            class="form-check-input me-1"
            :type="inputType"
            :value="item['@id']"
            :checked="item['@id'] in selectedProxy"
            :selected="item['@id'] in selectedProxy"
            v-model="selectedProxy"
            @change="checked"
            :disabled="isDisabled(item)"
          />
          <label
            :class="
              isDisabled(item) && isTraversable(item) ? '' : 'form-check-label'
            "
          >
            <ResolveIcon :item="item" :iconMapping="iconMapping" />
            <a
              v-if="item.is_folderish && isTraversable(item)"
              @click.prevent.stop="fetchData(item['@id'])"
              :href="item['@id']"
              class="list-group-item-action"
              >{{ item.title }}
              <span :class="`state-${item['review_state']}`">{{
                workflowTitleMapping[item["review_state"]]
              }}</span></a
            >
            <span v-else> {{ item.title }}
              <span :class="`state-${item['review_state']}`">{{
                workflowTitleMapping[item["review_state"]]
              }}</span>
            </span>
          </label>
        </div>
      </li>
    </template>
  </ul>
</template>
<script>
import ResolveIcon from "./ResolveIcon.vue";
export default {
  components: {
    ResolveIcon,
  },
  data() {
    return {
      selected: [],
    };
  },
  props: {
    items: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    selectedItems: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    inputType: {
      type: String,
      required: true,
      default: () => {
        return "checkbox";
      },
    },
    selectableTypes: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    traversableTypes: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    iconMapping: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
    workflowTitleMapping: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
    fetchData: {
      type: Function,
      required: true,
      default: () => {
        return null;
      },
    },
  },
  mounted() {
    this.selected = this.selectedItems;
  },
  methods: {
    checked() {
      this.$emit("checked", this.selected);
    },
    isDisabled(item) {
      return this.selectableTypes.indexOf(item.portal_type) == -1;
    },
    isTraversable(item) {
      return this.traversableTypes.indexOf(item.portal_type) != -1;
    },
  },
  computed: {
    selectedProxy: {
      get() {
        return this.selected;
      },
      set(value) {
        if (this.inputType == "checkbox") {
          this.selected = value;
        } else {
          this.selected = [value];
        }
      },
    },
  },
};
</script>
